# **salem_parser**
### A module used to parse reports from the Town of Salem Trial System into a format that can be easily used for data analysis.

# **Installing**
### **Python 3.6 or higher is required**

```
pip install salem_parser
```

# Example
```python
import salem_parser as salem

report = salem.parse_report(url)
for event in report.content:
    if event.type == "Message":
        print(event.author.role)
```