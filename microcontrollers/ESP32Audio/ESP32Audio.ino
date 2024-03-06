#include "header.h"
#include <EEPROM.h>

#define EEPROM_SIZE 512
const String DEFAULT_SERVER_NAME = "192.168.1.184";
const int DEFAULT_SERVER_PORT = 5000;
const String DEFAULT_SSID = "ANH MINH";
const String DEFAULT_PASSWORD = "ComTMM0112";

void from_rom(String &serverName, int &port, String &ssid, String &password) {
  serverName = EEPROM.readString(0);
  if(serverName.length() < 1) {
    Serial.println("LOG|Server name is not found in EEPROM. Using default server name.");
    serverName = DEFAULT_SERVER_NAME;
  }
  port = EEPROM.readInt(128);
  if(port == -1) {
    Serial.println("LOG|Server port is not found in EEPROM. Using default server port.");
    port = DEFAULT_SERVER_PORT;
  }
  ssid = EEPROM.readString(256);
  if(ssid.length() < 1) {
    Serial.println("LOG|WiFi ssid is not found in EEPROM. Using default ssid.");
    ssid = DEFAULT_SSID;
  }
  password = EEPROM.readString(384);
  if(password.length() < 1) {
    Serial.println("LOG|WiFi password is not found in EEPROM. Using default password.");
    password = DEFAULT_PASSWORD;
  }
}


void save(String serverName, int port, String ssid, String password) {
  Serial.println("LOG|Saving new input arguments");
  EEPROM.writeString(0, serverName);
  EEPROM.writeInt(128, port);
  EEPROM.writeString(256, ssid);
  EEPROM.writeString(384, password);
  EEPROM.commit();
}

void WiFiInit() {
  Serial.println("LOG|Using server: " + serverName + ":" + String(serverPort));
  Serial.println("LOG|Using WiFi: " + ssid + " Password: " + password);
  connectWiFi(ssid.c_str(), password.c_str());
}

void setup()
{
  Serial.begin(115200);
  Serial.println("DEVICE|ESP32MIC");
  if(!EEPROM.begin(EEPROM_SIZE)) {
    Serial.println("ERROR|EEPROM failed to initialise");
  } else {
    Serial.println("LOG|EEPROM initialise successfully");
  }
  from_rom(serverName, serverPort, ssid, password);

  // Serial.print("Enter serverName: ");
  // while (!Serial.available());
  // serverName = Serial.readString();
  // Serial.println("You entered: " + serverName);

  // Serial.print("Port: ");
  // while (!Serial.available());
  // serverPort = Serial.readString().toInt();
  // Serial.println("You entered: " + String(serverPort));
  
  WiFiInit();
  i2sInit();
  xTaskCreate(micTask, "micTask", 10000, NULL, 1, NULL);
  xTaskCreate(servoTask, "servoTask", 10000, NULL, 0, NULL);
}

void split(String src, String *&out, int &len, char delimiter = ' ', int max_len = 5)
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
      Serial.print("");
      if (id < max_len)
        out[id] = current.c_str();
      current = "";
      id++;
    }
    if (id >= max_len)
      return;
  }

  if (current.length() > 0 && id < max_len) {
    out[id] = current.c_str();
    id++;
  }

  len = id;
}

void(* resetFunc) (void) = 0;

void loop()
{
  if (Serial.available())
  {
    String command = Serial.readString();
    command.trim();
    int len = 0;
    String *args = NULL;
    split(command, args, len, ';');
    if(args == NULL || len < 1) {
      Serial.println("ERROR|Empty command");
      return;
    }
    String type = args[0];
    if(type.equalsIgnoreCase("RESET")) {
      resetFunc();
    }
    else if(type.equalsIgnoreCase("DEVICE")) {
      Serial.println("DEVICE|ESP32MIC");
    }
    else if(type.equalsIgnoreCase("INPUT")) {
      if(len != 5) {
        Serial.println("ERROR|Invalid input arguments. It should be INPUT;<server>;<port>;<ssid>;<password>");
        return;
      }
      serverName = args[1];
      serverPort = args[2].toInt();
      ssid = args[3];
      password = args[4];

      save(serverName, serverPort, ssid, password);

      WiFiInit();
    }
    else {
      Serial.println("ERROR|Invalid command type");
    }
  }
}
