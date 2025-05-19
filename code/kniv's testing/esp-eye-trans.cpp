#include <esp_camera.h>
#include <SPI.h>
#include <LoRa.h>

#define LORA_SS 18
#define LORA_RST 14
#define LORA_DIO0 26

#define MAX_CHUNK_SIZE 200
uint8_t frame_id = 0;

void setupCamera() {
  camera_config_t config = {
    .pin_pwdn = -1,
    .pin_reset = -1,
    .pin_xclk = 4,
    .pin_sscb_sda = 18,
    .pin_sscb_scl = 23,
    .pin_d7 = 36,
    .pin_d6 = 37,
    .pin_d5 = 38,
    .pin_d4 = 39,
    .pin_d3 = 35,
    .pin_d2 = 14,
    .pin_d1 = 13,
    .pin_d0 = 34,
    .pin_vsync = 5,
    .pin_href = 27,
    .pin_pclk = 25,
    .xclk_freq_hz = 20000000,
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    .pixel_format = PIXFORMAT_JPEG,
    .frame_size = FRAMESIZE_QVGA, // 160x120
    .jpeg_quality = 10,
    .fb_count = 1
  };

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed");
    while (1);
  }
}

void setupLoRa() {
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa init failed!");
    while (1);
  }
  Serial.println("LoRa init success");
}

void setup() {
  Serial.begin(115200);
  setupCamera();
  setupLoRa();
}

void loop() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) return;

  size_t total_len = fb->len;
  size_t chunks = (total_len + MAX_CHUNK_SIZE - 1) / MAX_CHUNK_SIZE;

  for (size_t i = 0; i < chunks; ++i) {
    size_t offset = i * MAX_CHUNK_SIZE;
    size_t size = min(MAX_CHUNK_SIZE, total_len - offset);

    LoRa.beginPacket();
    LoRa.write(frame_id);
    LoRa.write((uint8_t)i);
    LoRa.write((uint8_t)chunks);
    LoRa.write(fb->buf + offset, size);
    LoRa.endPacket();

    delay(100); // throttle slightly
  }

  Serial.printf("Sent frame %d (%d chunks)\n", frame_id, chunks);
  frame_id++;
  esp_camera_fb_return(fb);

  delay(2000); // next frame
}
