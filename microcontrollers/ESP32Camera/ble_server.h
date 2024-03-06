#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include "camera_web_server.h"

#define SERVER_NAME "TinyGuard ESP32"
#define SERVICE_UUID "e3091e1f-cdfa-49a3-95b4-f9b1746798aa"
#define WIFI_CHARACTERISTIC_UUID "23d69de0-cfaa-4b8d-86df-597e2f9b6260"

class WiFiCharacteristicCallbacks : public BLECharacteristicCallbacks
{
  void onWrite(BLECharacteristic *pCharacteristic)
  {
    std::string value = pCharacteristic->getValue();
    Serial.println(value.c_str());
    if (value.length() <= 0)
      return;
    Vector<String> wifiData = split(value.c_str(), ':');
    Serial.println(wifiData[0]);
    Serial.println(wifiData[1]);
  }
};

void _characteristicSetup(BLEService *pService)
{
  Serial.println("Creating WiFi Characteristic!");
  BLECharacteristic *pWifiChar = pService->createCharacteristic(WIFI_CHARACTERISTIC_UUID, BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE);
  pWifiChar->setCallbacks(new WiFiCharacteristicCallbacks());
}

void bleInit()
{
  Serial.println("Starting BLE work!");
  BLEDevice::init(SERVER_NAME);
  BLEServer *pServer = BLEDevice::createServer();
  Serial.println("Creating Service!");
  BLEService *pService = pServer->createService(SERVICE_UUID);
  _characteristicSetup(pService);

  Serial.println("Starting Service!");
  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
}