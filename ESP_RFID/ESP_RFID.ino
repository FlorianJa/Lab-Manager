#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h> // Read and write RFID using this library

// WiFi imports
#include <ESP8266WiFi.h>

// MQTT imports
#include <PubSubClient.h>

constexpr uint8_t RST_PIN = D3; // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D4;  // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN); // Instance of the class for RFID
MFRC522::MIFARE_Key key;

// MQTT topics to publish connect, disconnect messages which are subscribed by OctoPrint
const String connect_topic = "printer/connect";
const String disconnect_topic = "printer/disconnect";

String tag;

DynamicJsonBuffer jsonBuffer;

// Authentication LED for connecting printer to OctoPrint
// lights up when octoPrint is connected to printer i.e state is Operational in OctoPrint
const int OPERATION_LED = 5; // D1

// Status LED
// off if not printing
// on when printing
const int STATUS_LED = 4; // D2

// WLAN access data
// # WARNING add credentials
const char *ssid = "";
const char *password = "";

// MQTT server
// # WARNING add credentials
const char *mqtt_server = "";
const char *mqtt_user = "";
const char *mqtt_password = "";
const String mqtt_client = "Lab-ESP";

// MQTT init
WiFiClient espClient;
PubSubClient client(espClient);
// MQTT vars
long lastMsg = 0;
char msg[50];

void dump_byte_array(byte *buffer, byte bufferSize)
{
    for (byte i = 0; i < bufferSize; i++)
    {
        Serial.print(buffer[i] < 0x10 ? "0" : "");
        Serial.print(buffer[i], HEX);
    }
}

// Don't change the function below. This functions connects your ESP8266 to your router
void setup_wifi()
{
    delay(10);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");

    Serial.print("WiFi connected - ESP IP address: ");
    Serial.println(WiFi.localIP());
}

// callback procedure for MQTT subscribe
// Run through as soon as a message is pending
void callback(char *topic, byte *payload, unsigned int length)
{

    String msg = "";
    for (int i = 0; i < length; i++)
    {
        msg += (char)payload[i];
    }

    Serial.print(msg);
    JsonObject &data = jsonBuffer.parseObject(msg);
    Serial.println();

    // Turn the LED according to the message from topic: OctoPrintEvent/PrinterStateChanged publsihed by OctoPrint
    if (data["state_id"] == "STARTING")
    {
        Serial.print("Print start from Octoprint");
        Serial.print("Changing the LED state to");
        digitalWrite(STATUS_LED, HIGH);
        Serial.print("On");
        Serial.println();
    }
    else if (data["state_id"] == "CANCELLING" || data["state_id"] == "FINISHING")
    {
        Serial.print("Print end from Octoprint");
        Serial.print("Changing the LED state to");
        digitalWrite(STATUS_LED, LOW);
        Serial.print("Off");
        Serial.println();
        // Publish disconnect command to octoprint when print is finished or cancelled
        // To disconnect OctoPrint from Printer, i.e turns the state in OctoPrint to 'OFFLINE'
        Serial.print("Send MQTT disconnect:");
        String tmp = disconnect_topic;
        char disconnect_topic[tmp.length() + 1];
        tmp.toCharArray(disconnect_topic, tmp.length() + 1);
        tmp = "{\"_event\":\"DisconnectPrinter\",\"PrinterName\":\"EOS\"}";
        char msg[tmp.length() + 1];
        tmp.toCharArray(msg, tmp.length() + 1);
        client.publish(disconnect_topic, msg); // message is published, this message will be subscribed by OctoPrint to turn the state to 'OFFLINE'
        Serial.println(disconnect_topic);
        Serial.println(msg);
        Serial.println("Printer Disconnected from OctoPrint");
        digitalWrite(OPERATION_LED, LOW);
    }
    // Turn the LED according to the message from topic: OctoPrintEvent/PrinterStateChanged publsihed by OctoPrint
    else if (data["state_id"] == "OPERATIONAL")
    {
        Serial.print("Printer is connected");
        Serial.println();
        Serial.print("Changing the LED state to");
        digitalWrite(OPERATION_LED, HIGH);
        Serial.print(" On");
        Serial.println();
    }
    else if (data["state_id"] == "OFFLINE")
    {
        Serial.print("Printer is disconnected");
        Serial.println();
        Serial.print("Changing the LED state to");
        digitalWrite(OPERATION_LED, LOW);
        Serial.print(" Off");
        Serial.println();
    }
    Serial.println();
}

void setup()
{

    //LED Pins as OUTPUT setup
    pinMode(OPERATION_LED, OUTPUT);
    pinMode(STATUS_LED, OUTPUT);

    digitalWrite(OPERATION_LED, LOW);
    digitalWrite(STATUS_LED, LOW);

    // enable serial output
    Serial.begin(115200);
    Serial.println();
    Serial.println("Start FabLab ESP");

    // Init SPI bus
    Serial.println("SPI Init ...");
    SPI.begin();

    // Init MFRC522
    Serial.println("MFRC522 Init ...");
    mfrc522.PCD_Init();

    //WLAN start
    setup_wifi();

    // Your Domain name with URL path or IP address with path
    //MQTT client init
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);

    Serial.println(F("Lab ESP setup end...."));
    Serial.println(F("======================================================"));
}

void reconnect()
{
    // first test whether wifi works at all
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.print("WLAN connection interrupted ...");
        setup_wifi();
    }

    while (!client.connected())
    {
        Serial.print("Start MQTT connection ...");

        if (client.connect("EOSClient", mqtt_user, mqtt_password))
        {
            Serial.println("Connected to MQTT Server!");
            Serial.print("Subscribe to Topic ");
            Serial.println("");
            // Subscribes to MQTT Topic OctoPrintEvent/PrinterStateChanged which is published from OctoPrint
            client.subscribe("OctoPrintEvent/PrinterStateChanged");
        }
        else
        {
            // MQTT login failed, output error message
            Serial.print("failed:");
            switch (client.state())
            {
            case -4:
                Serial.print("MQTT_CONNECTION_TIMEOUT");
                break;
            case -3:
                Serial.print("MQTT_CONNECTION_LOST");
                break;
            case -2:
                Serial.print("MQTT_CONNECT_FAILED");
                break;
            case 1:
                Serial.print("MQTT_CONNECT_BAD_PROTOCOL");
                break;
            case 2:
                Serial.print("MQTT_CONNECT_BAD_CLIENT_ID");
                break;
            case 3:
                Serial.print("MQTT_CONNECT_UNAVAILABLE");
                break;
            case 4:
                Serial.print("MQTT_CONNECT_BAD_CREDENTIALS");
                break;
            case 5:
                Serial.print("MQTT_CONNECT_UNAUTHORIZED");
                break;
            }
            Serial.println("try again in 5 seconds ....");
        }
    }
}

void loop()
{
    if (!client.connected())
    {
        reconnect();
    }
    if (!client.loop())
    {
        client.connect("EOSClient", mqtt_user, mqtt_password);
    }

    // check if new RFID card is present
    if (!mfrc522.PICC_IsNewCardPresent())
        return;
    if (mfrc522.PICC_ReadCardSerial())
    {
        for (byte i = 0; i < 4; i++)
        {
            tag += mfrc522.uid.uidByte[i]; // Read the RFID tag number
        }
        Serial.println(tag);

        // When RFID is detected, Connect printer to OctoPrint
        // Publish connect command to octoprint when RFID tag number is detected
        // # WARNING add RFID tag
        if (tag == "")
        {
            Serial.println("Access granted");
            Serial.print("Send MQTT LOGIN:");
            String tmp = connect_topic;
            char connect_topic[tmp.length() + 1];
            tmp.toCharArray(connect_topic, tmp.length() + 1);
            tmp = "{\"_event\":\"ConnectPrinter\",\"PrinterName\":\"EOS\"}";
            char msg[tmp.length() + 1];
            tmp.toCharArray(msg, tmp.length() + 1);
            // Publish MQTT message to topic: printer/connect, to connect OctoPrint to Printer, i.e turns the state in OctoPrint to 'Operational'
            client.publish(connect_topic, msg);
            Serial.println(connect_topic);
            Serial.println(msg);
            Serial.println("Printer Connected to OctoPrint");
        }
        else
        {
            Serial.println("Access denied"); // When wrong RFID is detected
            delay(200);
        }
        tag = "";
        mfrc522.PICC_HaltA();
        mfrc522.PCD_StopCrypto1();
    }
}