#pragma once
#ifndef HEADER_H
#define HEADER_H

#include <WiFi.h>

extern String serverName;
extern String serverPath;
extern int serverPort;
extern WiFiClient client;
extern String ssid;
extern String password;

void i2s_adc_data_scale(uint8_t *d_buff, uint8_t *s_buff, uint32_t len);
void micTask(void *parameter);
void servoTask(void *parameter);
void wavHeader(byte *header, int wavSize);
String sendAudio();
void connectWiFi(const char*, const char*);
void i2sInit();

#endif
