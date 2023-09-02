from bs4 import BeautifulSoup, ResultSet
from pydantic import HttpUrl, parse_obj_as
from selenium import webdriver

from logfetcher.cruds.processros import find_character_id
from logfetcher.models.characters import Character, CharacterCreate
