import xml.etree.ElementTree as ET
import re
import os

class UIElement:
    def __init__(self, node):
        self.node = node
        self.text = node.attrib.get('text', '')
        self.resource_id = node.attrib.get('resource-id', '')
        self.content_desc = node.attrib.get('content-desc', '')
        self.class_name = node.attrib.get('class', '')
        self.bounds = self._parse_bounds(node.attrib.get('bounds', '[0,0][0,0]'))

    def _parse_bounds(self, bounds_str):
        """Parses '[x1,y1][x2,y2]' -> (x1, y1, x2, y2)"""
        coords = [int(x) for x in re.findall(r'\d+', bounds_str)]
        return coords # [x1, y1, x2, y2]

    @property
    def center(self):
        x1, y1, x2, y2 = self.bounds
        return (x1 + x2) // 2, (y1 + y2) // 2

    @property
    def top_10_center(self):
        """Refined targeting to hit the header/title area of Compose cards."""
        x1, y1, x2, y2 = self.bounds
        center_x = (x1 + x2) // 2
        # Target the top 10% of the element (as requested for card titles)
        top_y = y1 + (y2 - y1) // 10
        return center_x, top_y

class UIEngine:
    def __init__(self, driver):
        self.driver = driver

    def get_elements(self):
        """Fetch current hierarchy and parse into UIElement objects."""
        xml_path = self.driver.get_hierarchy()
        if not os.path.exists(xml_path):
            return []
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            return [UIElement(node) for node in root.findall('.//node')]
        except Exception as e:
            print(f"Error parsing hierarchy: {e}")
            return []

    def find_element(self, text=None, resource_id=None, content_desc=None, timeout=10):
        """Find an element with polling."""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            elements = self.get_elements()
            for el in elements:
                if text and text in el.text: return el
                if resource_id and resource_id in el.resource_id: return el
                if content_desc and content_desc in el.content_desc: return el
            time.sleep(0.5)
        return None

    def wait_until_gone(self, text=None, resource_id=None, timeout=10):
        """Wait for an element to disappear."""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            found = False
            elements = self.get_elements()
            for el in elements:
                if text and text in el.text: found = True; break
                if resource_id and resource_id in el.resource_id: found = True; break
            if not found:
                return True
            time.sleep(0.5)
        return False
