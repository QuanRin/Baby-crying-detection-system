enum Flavor {
  development,
  staging,
  production,
}

enum Level {
  error,
  warn,
  info,
  debug,
  trace,
}

enum BottomTabItem {
  home,
  search,
  favorite,
  profile,
}

enum City {
  osaka,
  kyoto,
  hyogo,
  shiga,
  nara,
  wakayama,
}

enum DatePickerEnum {
  year,
  month,
  day,
}

extension DatePickerEnumExtension on DatePickerEnum {
  int get getLengthRender {
    switch (this) {
      case DatePickerEnum.year:
        return 9001;
      case DatePickerEnum.month:
        return 12;
      case DatePickerEnum.day:
        return 31;
    }
  }

  bool get isYear => this == DatePickerEnum.year;
}

enum PaymentMethod {
  cash,
  visa,
}

enum BabyStatus {
  noise,
  crying,
  laugh,
  silence,
}

extension BabyStatusExtension on BabyStatus {
  String get statusString {
    switch (this) {
      case BabyStatus.noise:
        return 'Noise';
      case BabyStatus.crying:
        return 'Crying';
      case BabyStatus.laugh:
        return 'Laugh';
      case BabyStatus.silence:
        return 'Silence';
    }
  }
}

enum UsePoint {
  fullPoint,
  manual,
}
