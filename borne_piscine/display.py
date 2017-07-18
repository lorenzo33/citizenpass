#!/usr/bin/python
# -*- coding:utf8 -*-

############################################
#  ____ ___ ____  ____  _        _ __   __
# |  _ \_ _/ ___||  _ \| |      / \\ \ / /
# | | | | |\___ \| |_) | |     / _ \\ V / 
# | |_| | | ___) |  __/| |___ / ___ \| |  
# |____/___|____/|_|   |_____/_/   \_\_|  
#
############################################                                        

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time
import logging

# Definit le numero des broche pour la connexion (BOARD MODE)
LCD_RS = 37 # GPIO26 : Register select (select command mode - 0, or data mode - 1)
LCD_E  = 35 # GPIO19 : Enabled
LCD_D4 = 33 # GPIO13 : D4 
LCD_D5 = 31 # GPIO06 : D5
LCD_D6 = 29 # GPIO05 : D6
LCD_D7 = 32 # GPIO12 : D7

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def lcd_init():
  GPIO.setmode(GPIO.BOARD)     # Use BCM BOARD numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcdWriteByte(0x33,LCD_CMD)
  lcdWriteByte(0x32,LCD_CMD)
  lcdWriteByte(0x28,LCD_CMD)
  lcdWriteByte(0x0C,LCD_CMD)
  lcdWriteByte(0x06,LCD_CMD)
  lcdWriteByte(0x01,LCD_CMD)
  logging.info("Affichage initialisé")

def lcdWriteFirstLine(text):
    lcdWriteByte(LCD_LINE_1, LCD_CMD)
    lcdWriteString(text)

def lcdWriteSecondLine(text):
    lcdWriteByte(LCD_LINE_2, LCD_CMD)

def lcdWriteString(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcdWriteByte(ord(message[i]),LCD_CHR)

def lcdWriteByte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)