from typing import List, Optional
from jinja2 import Template


class Source:
    """External data source for feature. Typically a 'table'.
     Attributes:
         name: name of the source
         event_timestamp_column: column name of the event timestamp
         timestamp_format: the format of the event_timestamp_column, e.g. yyyy/MM/DD.
    """
    def __init__(self,
                 name: str,
                 event_timestamp_column: Optional[str], 
                 timestamp_format: Optional[str] = "epoch") -> None:
        self.name = name
        self.event_timestamp_column = event_timestamp_column
        self.timestamp_format = timestamp_format

class PassthroughSource(Source):
    """A type of 'passthrough' source, a.k.a. request feature source.
    """
    SOURCE_NAME = "PASSTHROUGH"
    def __init__(self) -> None:
        super().__init__(self.SOURCE_NAME, None, None)

    def to_feature_config(self) -> str:
        return "source: " + self.name

class HdfsSource(Source):
    """A data source(table) stored on HDFS-like file system. Data can be fetch through a POSIX style path."""
    def __init__(self, name: str, path: str, event_timestamp_column: Optional[str], timestamp_format: Optional[str] = "epoch") -> None:
        super().__init__(name, event_timestamp_column, timestamp_format)
        self.path = path

    def to_feature_config(self) -> str:
        tm = Template("""  
            {{source.name}}: {
                location: {path: "{{source.path}}"}
                {% if source.event_timestamp_column is defined %}
                    timeWindowParameters: {
                        timestampColumn: "{{source.event_timestamp_column}}"
                        timestampColumnFormat: "{{source.timestamp_format}}"
                    }
                {% endif %}
            } 
        """)
        msg = tm.render(source = self)
        return msg
    
PASSTHROUGH_SOURCE = PassthroughSource()