from data import TinyGuardianBabyDataset
import torch.nn as nn
import torch

image_darknet_config = [
    ('Conv', (7, 64, 2, 3)),
    'M',
    ('Conv', (3, 192, 1, 1)),
    'M',
    ('Conv', (1, 128, 1, 0)),
    ('Conv', (3, 256, 1, 1)),
    ('Conv', (1, 256, 1, 0)),
    ('Conv', (1, 512, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 256, 1, 0), (3, 512, 1, 1)],
        4
    ),
    ('Conv', (1, 512, 1, 0)),
    ('Conv', (3, 1024, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 512, 1, 0), (3, 1024, 1, 1)],
        2
    ),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 2, 1)),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 1, 1)),
]

audio_darknet_config = [
    ('Conv', (5, 64, 2, 3)),
    'M',
    ('Conv', (1, 128, 1, 0)),
    ('Conv', (3, 256, 1, 1)),
    ('Conv', (1, 256, 1, 0)),
    ('Conv', (1, 512, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 256, 1, 0), (3, 512, 1, 1)],
        4
    ),
    ('Conv', (1, 512, 1, 0)),
    ('Conv', (3, 1024, 1, 1)),
    'M',
    (
        'MultiConv',
        [(1, 512, 1, 0), (3, 1024, 1, 1)],
        2
    ),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 2, 1)),
    ('Conv', (3, 1024, 1, 1)),
    ('Conv', (3, 1024, 1, 1)),
]


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, bn_act=True, **kwargs) -> None:
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels,
                              bias=not bn_act, **kwargs)
        self.batchNorm = nn.BatchNorm2d(out_channels)
        self.leakyRelu = nn.LeakyReLU(0.1)
        self.use_bn_act = bn_act

    def forward(self, x):
        if self.use_bn_act:
            return self.leakyRelu(self.batchNorm(self.conv(x)))
        else:
            return self.conv(x)


class ResidualBlock(nn.Module):
    def __init__(self, channels, use_residual=True, num_repeats=1):
        super().__init__()
        self.layers = nn.ModuleList()
        for _ in range(num_repeats):
            self.layers += [
                nn.Sequential(
                    CNNBlock(channels, channels // 2, kernel_size=1),
                    CNNBlock(channels // 2, channels,
                             kernel_size=3, padding=1),
                )
            ]

        self.use_residual = use_residual
        self.num_repeats = num_repeats

    def forward(self, x):
        for layer in self.layers:
            if self.use_residual:
                x = x + layer(x)
            else:
                x = layer(x)

        return x


class YoloV1(nn.Module):
    def __init__(self, split_size, num_boxes,
                 num_classes, in_channels=3) -> None:
        super(YoloV1, self).__init__()
        self.architecture = image_darknet_config
        self.in_channels = in_channels
        self.darknet = self._build_from_arch(self.architecture, in_channels)
        self.fcs = self._build_fcs(split_size, num_boxes,
                                   num_classes)

    def forward(self, x):
        x = self.darknet(x)
        return self.fcs(torch.flatten(x, start_dim=1))

    def _build_from_arch(self, architecture, in_channels):
        layers = []
        for x in architecture:
            if type(x) == tuple:
                archType = x[0]
                if archType == 'Conv':
                    layers.append(
                        CNNBlock(
                            in_channels, x[1][1], kernel_size=x[1][0], stride=x[1][2], padding=x[1][3])
                    )

                    in_channels = x[1][1]
                elif archType == 'MultiConv':
                    for _ in range(x[2]):
                        for conv in x[1]:
                            layers.append(
                                CNNBlock(
                                    in_channels, conv[1], kernel_size=conv[0], stride=conv[2], padding=conv[3])
                            )
                            in_channels = conv[1]
            elif type(x) == str:
                layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
        return nn.Sequential(*layers)

    def _build_fcs(self, split_size, num_boxes, num_classes):
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 496),
            nn.Dropout(0.0),
            nn.LeakyReLU(0.1),
            nn.Linear(496, S * S * (C + B * 5))
        )


class TinyGuardian(YoloV1):
    def __init__(self, split_size, num_boxes,
                 num_classes, aud_out_extra, img_in_channels=3, aud_in_channels=1) -> None:
        super(TinyGuardian, self).__init__(split_size, num_boxes,
                                           num_classes, in_channels=img_in_channels)
        self.img_architecture = image_darknet_config
        self.aud_architecture = audio_darknet_config
        self.aud_in_channels = aud_in_channels
        self.keep_rate = 0.5
        self.aud_darknet = self._build_from_arch(
            audio_darknet_config, aud_in_channels)
        self.fcs = self.__build_fcs(
            split_size, num_boxes, num_classes, aud_vec_extra=4*4*1024, aud_out_extra=aud_out_extra)
    #     self.fcs = self._build_fcs(**kwargs)

    def __build_fcs(self, split_size, num_boxes, num_classes, aud_vec_extra, aud_out_extra):
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S + aud_vec_extra, 496),
            nn.Dropout(self.keep_rate),
            nn.LeakyReLU(0.1),
            nn.Linear(496, S * S * (C + B * 5) + aud_out_extra)
        )

    def forward(self, img, aud):
        img_output = self.darknet(img)
        img_vec = torch.flatten(img_output, start_dim=1)
        aud_output = self.aud_darknet(aud)
        aud_vec = torch.flatten(aud_output, start_dim=1)
        concat_vec = torch.cat((img_vec, aud_vec), dim=1)
        return self.fcs(concat_vec)


if __name__ == "__main__":

    # model = YoloV1(split_size=7, num_boxes=2, num_classes=2)
    model2 = TinyGuardian(split_size=7, num_boxes=2,
                          num_classes=2, aud_out_extra=3)
    dataset = TinyGuardianBabyDataset()
    img, aud, img_target, aud_target = dataset[700]
    out = model2(img.unsqueeze(0), aud.unsqueeze(0))
    from loss import TinyGuardianLoss
    loss_fn = TinyGuardianLoss()
    l = loss_fn(out, img_target.unsqueeze(0), aud_target.unsqueeze(0))
