import xml.etree.ElementTree as ET

async def receive_data(url):
    """Download chunks of bytes from the URL asynchronously."""
    yield b"<svg "
    yield b"viewBox=\"-105 -100 210 270\""
    yield b"></svg>"

async def parse(url, events=None):
    parser = ET.XMLPullParser(events)
    async for chunk in receive_data(url):
        parser.feed(chunk)
        for event, element in parser.read_events():
            yield event, element
            print (event, element)