#pragma once
#include <Arduino.h>
#include <WiFi.h>

#ifndef CAMERA_WEB_SERVER_H
#define CAMERA_WEB_SERVER_H

extern String serverName;
extern int serverPort;
extern String ssid;
extern String password;
void connectWiFi(String ssid, String password);
void webServerInit();
void webServerLoop();
void startCameraServer();

#endif