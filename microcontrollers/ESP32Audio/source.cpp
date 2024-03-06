#pragma once
#include "header.h"
String ssid = "BEAN HONG COFFEE - 2.4Ghz";
String password = "11119999";
String serverName = "192.168.5.22";
String serverPath = "/api/device/audio_input";
int serverPort = 5000;
WiFiClient client;

#include <driver/i2s.h>
#define I2S_WS 13
#define I2S_SD 15
#define I2S_SCK 12
#define I2S_PORT I2S_NUM_0
#define I2S_SAMPLE_RATE (16000)
#define I2S_SAMPLE_BITS (16)
#define I2S_READ_LEN (16 * 1024)
#define RECORD_TIME (5)
#define I2S_CHANNEL_NUM (1)
#define FLASH_RECORD_SIZE (I2S_CHANNEL_NUM * I2S_SAMPLE_RATE * I2S_SAMPLE_BITS / 8 * RECORD_TIME)
const int headerSize = 44;

#include <ESP32Servo.h>
#include <math.h>
#define SERVO_PIN 14
float A = 45;
float OFFSET = A;
float G = 9.8;
float L = 0.01;
Servo servo;
bool is_crying = false;

#include <ArduinoJson.h>

void i2sInit()
{
  i2s_config_t i2s_config = {
      .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
      .sample_rate = I2S_SAMPLE_RATE,
      .bits_per_sample = i2s_bits_per_sample_t(I2S_SAMPLE_BITS),
      .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
      .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_I2S | I2S_COMM_FORMAT_I2S_MSB),
      .intr_alloc_flags = 0,
      .dma_buf_count = 16,
      .dma_buf_len = 512,
      .use_apll = 0};

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);

  const i2s_pin_config_t pin_config = {
      .bck_io_num = I2S_SCK,
      .ws_io_num = I2S_WS,
      .data_out_num = -1,
      .data_in_num = I2S_SD};

  i2s_set_pin(I2S_PORT, &pin_config);
}
void connectWiFi(const char *ssid, const char *password)
{
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    if (Serial.available())
      return;
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("LOG|WiFi connected");
}
void wavHeader(byte *header, int wavSize)
{
  header[0] = 'R';
  header[1] = 'I';
  header[2] = 'F';
  header[3] = 'F';
  unsigned int fileSize = wavSize + headerSize - 8;
  header[4] = (byte)(fileSize & 0xFF);
  header[5] = (byte)((fileSize >> 8) & 0xFF);
  header[6] = (byte)((fileSize >> 16) & 0xFF);
  header[7] = (byte)((fileSize >> 24) & 0xFF);
  header[8] = 'W';
  header[9] = 'A';
  header[10] = 'V';
  header[11] = 'E';
  header[12] = 'f';
  header[13] = 'm';
  header[14] = 't';
  header[15] = ' ';
  header[16] = 0x10;
  header[17] = 0x00;
  header[18] = 0x00;
  header[19] = 0x00;
  header[20] = 0x01;
  header[21] = 0x00;
  header[22] = 0x01;
  header[23] = 0x00;
  header[24] = 0x80;
  header[25] = 0x3E;
  header[26] = 0x00;
  header[27] = 0x00;
  header[28] = 0x00;
  header[29] = 0x7D;
  header[30] = 0x00;
  header[31] = 0x00;
  header[32] = 0x02;
  header[33] = 0x00;
  header[34] = 0x10;
  header[35] = 0x00;
  header[36] = 'd';
  header[37] = 'a';
  header[38] = 't';
  header[39] = 'a';
  header[40] = (byte)(wavSize & 0xFF);
  header[41] = (byte)((wavSize >> 8) & 0xFF);
  header[42] = (byte)((wavSize >> 16) & 0xFF);
  header[43] = (byte)((wavSize >> 24) & 0xFF);
}

String sendAudio()
{
  String getAll;
  String getBody;

  Serial.println("Connecting to server: " + serverName + ":" + String(serverPort));

  if (client.connect(serverName.c_str(), serverPort))
  {
    Serial.println("Connection successful!");
    String head = "--RandomNerdTutorials\r\nContent-Disposition: form-data; name=\"audioFile\"; filename=\"esp32-audio.wav\"\r\nContent-Type: */*\r\n\r\n";
    String tail = "\r\n--RandomNerdTutorials--\r\n";

    uint32_t length = head.length() + FLASH_RECORD_SIZE + headerSize + tail.length();
    client.println("POST " + serverPath + " HTTP/1.1");
    client.println("Host: " + serverName);
    client.println("Content-Length: " + String(length));
    client.println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
    client.println();
    client.print(head);

    byte header[headerSize];
    wavHeader(header, FLASH_RECORD_SIZE);

    client.write((char *)header, headerSize);

    int i2s_read_len = I2S_READ_LEN;
    int flash_wr_size = 0;
    size_t bytes_read;

    char *i2s_read_buff = (char *)calloc(i2s_read_len, sizeof(char));
    uint8_t *flash_write_buff = (uint8_t *)calloc(i2s_read_len, sizeof(char));

    i2s_read(I2S_PORT, (void *)i2s_read_buff, i2s_read_len, &bytes_read, portMAX_DELAY);
    i2s_read(I2S_PORT, (void *)i2s_read_buff, i2s_read_len, &bytes_read, portMAX_DELAY);

    Serial.println(" *** Recording Start *** ");
    while (flash_wr_size < FLASH_RECORD_SIZE)
    {
      i2s_read(I2S_PORT, (void *)i2s_read_buff, min(i2s_read_len, FLASH_RECORD_SIZE - flash_wr_size), &bytes_read, portMAX_DELAY);

      i2s_adc_data_scale(flash_write_buff, (uint8_t *)i2s_read_buff, min(i2s_read_len, FLASH_RECORD_SIZE - flash_wr_size));
      client.write((const char *)flash_write_buff, min(i2s_read_len, FLASH_RECORD_SIZE - flash_wr_size));
      flash_wr_size += min(i2s_read_len, FLASH_RECORD_SIZE - flash_wr_size);
      ets_printf("Sound recording %u%%\n", flash_wr_size * 100 / FLASH_RECORD_SIZE);
      ets_printf("Never Used Stack Size: %u\n", uxTaskGetStackHighWaterMark(NULL));
      Serial.print((char)flash_write_buff[0]);
    }
    // file.close();

    free(i2s_read_buff);
    i2s_read_buff = NULL;
    free(flash_write_buff);
    flash_write_buff = NULL;

    client.print(tail);

    int timoutTimer = 5000;
    long startTimer = millis();
    boolean state = false;

    while ((startTimer + timoutTimer) > millis())
    {
      Serial.print(".");
      delay(100);
      while (client.available())
      {
        char c = client.read();
        if (c == '\n')
        {
          if (getAll.length() == 0)
          {
            state = true;
          }
          getAll = "";
        }
        else if (c != '\r')
        {
          getAll += String(c);
        }
        if (state == true)
        {
          getBody += String(c);
        }
        startTimer = millis();
      }
      if (getBody.length() > 0)
      {
        break;
      }
    }
    Serial.println();
    client.stop();
    Serial.println(getBody);
  }
  else
  {
    getBody = "Connection to " + serverName + " failed.";
    Serial.println(getBody);
  }
  return getBody;
}
void i2s_adc_data_scale(uint8_t *d_buff, uint8_t *s_buff, uint32_t len)
{
  uint32_t j = 0;
  uint32_t dac_value = 0;
  for (int i = 0; i < len; i += 2)
  {
    dac_value = ((((uint16_t)(s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
    d_buff[j++] = 0;
    d_buff[j++] = dac_value * 256 / 2048;
  }
}

int intensityCheck()
{

  int i2s_read_len = 16000 * 0.5;
  int16_t *i2s_read_buff = (int16_t *)calloc(i2s_read_len, sizeof(int16_t));
  size_t bytes_read;

  if (i2s_read_buff == nullptr)
  {
    free(i2s_read_buff);
    i2s_read_buff = NULL;
    return 0;
  }

  i2s_read(I2S_PORT, (void *)i2s_read_buff, i2s_read_len * sizeof(int16_t), &bytes_read, portMAX_DELAY);
  i2s_read(I2S_PORT, (void *)i2s_read_buff, i2s_read_len * sizeof(int16_t), &bytes_read, portMAX_DELAY);
  if (i2s_read_buff == nullptr)
  {
    free(i2s_read_buff);
    i2s_read_buff = NULL;
    return 0;
  }

  float STE = 0;
  for (size_t i = 0; i < bytes_read / sizeof(int16_t); i++)
  {
    int16_t value = i2s_read_buff[i];
    STE += ((float)value / 1000) * ((float)value / 1000);
  }

  free(i2s_read_buff);
  i2s_read_buff = NULL;

  return STE;
}

void micTask(void *parameter)
{

  i2sInit();
  i2s_start(I2S_PORT);

  // size_t bytesIn = 0;
  while (1)
  {
    if(WiFi.status() != WL_CONNECTED)
      continue;
    float intensity = intensityCheck();
    Serial.println(intensity);
    if (intensity < 200 && !is_crying) {
      is_crying = false;
      continue;
    }
    String result = sendAudio();
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, result);
    if (error)
    {
      Serial.println("Error decoding response");
      continue;
    }
    if(doc["result"].containsKey("is_crying")) {
      is_crying = doc["result"]["is_crying"];
    } else {
      is_crying = false;
    }
    delay(10);
  }
}
float angle = 0;
void servoInit()
{
  pinMode(SERVO_PIN, OUTPUT);
  servo.attach(SERVO_PIN);
}

void lerpTo(float target, float weight = 0.5, float eps = 1e-3, int delay_time = 20)
{
  while (fabs(target - angle) > eps)
  {
    angle = angle * weight + target * (1 - weight);
    int servoAngle = (int)angle;
    servo.write((int)OFFSET + servoAngle);
    delay(delay_time);
  }
}

void swing_step(float &angle, float &vtheta, float time_step = 0.01)
{
  float atheta = -G / L * sin(angle * 3.14 / 180.0);
  vtheta += atheta * time_step;
  angle += vtheta * time_step;
}

void servoTask(void *parameter)
{
  pinMode(27, OUTPUT);
  digitalWrite(27, HIGH);
  servoInit();
  while (1)
  {
    if (is_crying)
    {
      lerpTo(A);
      float vtheta = 0;
      while (is_crying)
      {
        swing_step(angle, vtheta);
        int servoAngle = (int)angle;
        servo.write((int)OFFSET + servoAngle);
        // Serial.print("Swinging ");
        // Serial.println(servoAngle);
        delay(20);
      }
    }
    else
    {
      lerpTo(0);
    }
    delay(20);
  }
}