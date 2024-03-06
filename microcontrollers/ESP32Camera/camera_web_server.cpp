#include "camera_web_server.h"
#include "esp_camera.h"
#include <WiFiClientSecure.h>
#include "esp_wifi.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include "fb_gfx.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_http_server.h"

String ssid = "BEAN HONG COFFEE - 2.4Ghz";
String password = "11119999";

String serverName = "192.168.5.165";

typedef struct
{
  httpd_req_t *req;
  size_t len;
} jpg_chunking_t;

#define PART_BOUNDARY "123456789000000000000987654321"
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27

#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

#define LED_GPIO_NUM 4

camera_fb_t *fb = NULL;

void startCameraServer();
void setupLedFlash(int pin);


String imageServerPath = "/api/device/image_input";

int serverPort = 5000;

WiFiClient client;
WiFiClientSecure client_secure;

const int timerInterval = 100;
unsigned long previousMillis = 0;

String sendPhoto()
{
  WiFiClient *_client = &client;
  int port = serverPort;

  String getAll;
  String getBody;
  Serial.println("Connecting to server: " + serverName + ":" + String(serverPort));

  if (_client->connect(serverName.c_str(), port))
  {
    Serial.println("Connection successful!");
  } else {
    getBody = "Connection to " + serverName + " failed.";
    Serial.println(getBody);
    return getBody;
  }

  fb = esp_camera_fb_get();
  if (!fb)
  {
    Serial.println("Camera capture failed");
    delay(1000);
    ESP.restart();
  }

  String head = "--RandomNerdTutorials\r\nContent-Disposition: form-data; name=\"imageFile\"; filename=\"esp32-cam.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
  String tail = "\r\n--RandomNerdTutorials--\r\n";

  uint32_t imageLen = fb->len;
  uint32_t extraLen = head.length() + tail.length();
  uint32_t totalLen = imageLen + extraLen;

  _client->println("POST " + imageServerPath + " HTTP/1.1");
  _client->println("Host: " + serverName);
  _client->println("Content-Length: " + String(totalLen));
  _client->println("Content-Type: multipart/form-data; boundary=RandomNerdTutorials");
  _client->println();
  _client->print(head);

  uint8_t *fbBuf = fb->buf;
  size_t fbLen = fb->len;
  for (size_t n = 0; n < fbLen; n = n + 1024)
  {
    if (n + 1024 < fbLen)
    {
      _client->write(fbBuf, 1024);
      fbBuf += 1024;
    }
    else if (fbLen % 1024 > 0)
    {
      size_t remainder = fbLen % 1024;
      _client->write(fbBuf, remainder);
    }
  }
  _client->print(tail);

  esp_camera_fb_return(fb);

  int timoutTimer = 5000;
  long startTimer = millis();
  boolean state = false;

  while ((startTimer + timoutTimer) > millis())
  {
    Serial.print(".");
    delay(100);
    while (_client->available())
    {
      char c = _client->read();
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
  _client->stop();
  Serial.println(getBody);
  return getBody;
}

esp_err_t camInit()
{
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG;
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 8;
  config.fb_count = 1;

  setupLedFlash(LED_GPIO_NUM);

  esp_err_t err = esp_camera_init(&config);
  return err;
}

void camTask(void *parameter)
{
  esp_err_t err = camInit();
  if (err != ESP_OK)
  {
    Serial.printf("Camera init failed with error 0x%x", err);
  }
  else
  {
    // Start streaming web server
    startCameraServer();
    Serial.print("Camera Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.println("' to connect");
    while (1)
    {
      if (WiFi.status() == WL_CONNECTED)
      {
        unsigned long currentMillis = millis();
        if (currentMillis - previousMillis >= timerInterval)
        {
          sendPhoto();
          previousMillis = currentMillis;
        }
      }
    }
  }
}

void webServerInit()
{
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  xTaskCreate(camTask, "camTask", 10000, NULL, 1, NULL);
}

void connectWiFi(String ssid, String password)
{
  Serial.println("Detecting new WiFi connection request! Reconnecting...");
  WiFi.disconnect();
  WiFi.begin(ssid, password);
  WiFi.softAP(ssid, password);
  Serial.println("Connecting to:");
  Serial.println("SSID: " + ssid);
  Serial.println("Password: " + password);
  WiFi.setSleep(false);

  int TIME_OUT = 100;
  int t = 0;

  while (WiFi.status() != WL_CONNECTED)
  {
    if (t >= TIME_OUT)
    {
      Serial.println("Connection timeout!");
      return;
    }
    delay(500);
    Serial.print(".");
    t++;
    if (Serial.available())
      return;
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void split(String src, String *&out, char delimiter = ' ', int max_len = 2)
{
  out = new String[max_len];
  int id = 0;
  String current = "";
  for (char c : src)
  {
    if (c != delimiter)
      current += c;
    else
    {
      if (id < max_len)
        out[id] = current.c_str();
      current = "";
      id++;
    }
    if (id >= max_len)
      return;
  }

  if (current.length() > 0 && id < max_len)
    out[id] = current.c_str();
}

void webServerLoop()
{

}
