"""
AEONCOSMA BI Platform Integration
================================
Configurações e conectores para plataformas de Business Intelligence
"""

import json
import yaml
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from pathlib import Path

@dataclass
class DatabaseConnection:
    """Configuração de conexão com banco de dados"""
    host: str
    database: str
    username: str
    password: str
    port: int = 5432
    driver: str = "postgresql"
    
@dataclass
class SupersetConfig:
    """Configuração para Apache Superset"""
    base_url: str
    username: str
    password: str
    database_connections: List[DatabaseConnection]
    dashboards: List[Dict[str, Any]]
    
@dataclass
class MetabaseConfig:
    """Configuração para Metabase"""
    host: str
    username: str
    password: str
    database_id: int
    port: int = 3000
    
@dataclass
class GrafanaConfig:
    """Configuração para Grafana"""
    host: str
    api_key: str
    datasources: List[Dict[str, Any]]
    dashboards: List[str]
    port: int = 3000

class BIPlatformIntegration:
    """Integração com plataformas de BI"""
    
    def __init__(self, config_path: str = "bi_config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo YAML"""
        config_file = Path(self.config_path)
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Cria configuração padrão"""
        default_config = {
            'superset': {
                'base_url': 'http://localhost:8088',
                'username': 'admin',
                'password': 'admin',
                'database_connections': [
                    {
                        'host': 'localhost',
                        'port': 5432,
                        'database': 'aeoncosma',
                        'username': 'aeoncosma_user',
                        'password': 'secure_password',
                        'driver': 'postgresql'
                    }
                ]
            },
            'metabase': {
                'host': 'localhost',
                'port': 3000,
                'username': 'admin@aeoncosma.com',
                'password': 'secure_password',
                'database_id': 1
            },
            'grafana': {
                'host': 'localhost',
                'port': 3000,
                'api_key': 'your_grafana_api_key_here',
                'datasources': [
                    {
                        'name': 'AEONCOSMA_Metrics',
                        'type': 'prometheus',
                        'url': 'http://localhost:9090'
                    },
                    {
                        'name': 'AEONCOSMA_Logs',
                        'type': 'loki',
                        'url': 'http://localhost:3100'
                    }
                ]
            }
        }
        
        # Salvar configuração padrão
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
            
        return default_config
    
    def generate_superset_dashboard_config(self) -> Dict[str, Any]:
        """Gera configuração de dashboard para Superset"""
        return {
            "dashboard_title": "AEONCOSMA System Overview",
            "description": "Comprehensive view of AEONCOSMA network performance",
            "charts": [
                {
                    "chart_type": "line",
                    "title": "Node Performance Over Time",
                    "datasource": "aeoncosma_metrics",
                    "metrics": ["cpu_usage", "memory_usage", "network_latency"],
                    "groupby": ["node_type"],
                    "time_range": "7 days"
                },
                {
                    "chart_type": "heatmap", 
                    "title": "Network Topology Heat Map",
                    "datasource": "aeoncosma_topology",
                    "metrics": ["connection_strength"],
                    "groupby": ["source_node", "target_node"]
                },
                {
                    "chart_type": "sankey",
                    "title": "Energy Flow Visualization",
                    "datasource": "aeoncosma_energy",
                    "metrics": ["energy_flow"],
                    "groupby": ["source", "target"]
                },
                {
                    "chart_type": "3d_scatter",
                    "title": "3D Node Distribution",
                    "datasource": "aeoncosma_positions",
                    "x_axis": "x_coordinate",
                    "y_axis": "y_coordinate", 
                    "z_axis": "z_coordinate",
                    "size_metric": "importance_score",
                    "color_metric": "node_type"
                }
            ],
            "filters": [
                {
                    "column": "node_type",
                    "type": "select",
                    "multiple": True
                },
                {
                    "column": "timestamp",
                    "type": "datetime_range"
                }
            ]
        }
    
    def generate_grafana_dashboard_json(self) -> Dict[str, Any]:
        """Gera JSON de dashboard para Grafana"""
        return {
            "dashboard": {
                "id": None,
                "title": "AEONCOSMA Real-time Monitoring",
                "tags": ["aeoncosma", "network", "blockchain"],
                "timezone": "browser",
                "panels": [
                    {
                        "id": 1,
                        "title": "System CPU Usage",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "aeoncosma_cpu_usage",
                                "legendFormat": "{{node_type}} - {{instance}}"
                            }
                        ],
                        "gridPos": {"h": 9, "w": 12, "x": 0, "y": 0}
                    },
                    {
                        "id": 2,
                        "title": "Memory Usage Distribution",
                        "type": "piechart",
                        "targets": [
                            {
                                "expr": "aeoncosma_memory_usage",
                                "legendFormat": "{{node_type}}"
                            }
                        ],
                        "gridPos": {"h": 9, "w": 12, "x": 12, "y": 0}
                    },
                    {
                        "id": 3,
                        "title": "Network Consensus Rate",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "rate(aeoncosma_consensus_total[5m])",
                                "legendFormat": "Consensus/sec"
                            }
                        ],
                        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 9}
                    },
                    {
                        "id": 4,
                        "title": "Active Nodes",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "aeoncosma_active_nodes",
                                "legendFormat": "Active Nodes"
                            }
                        ],
                        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 9}
                    },
                    {
                        "id": 5,
                        "title": "Network Health Score",
                        "type": "gauge",
                        "targets": [
                            {
                                "expr": "aeoncosma_health_score",
                                "legendFormat": "Health %"
                            }
                        ],
                        "fieldConfig": {
                            "defaults": {
                                "min": 0,
                                "max": 100,
                                "thresholds": {
                                    "steps": [
                                        {"color": "red", "value": 0},
                                        {"color": "yellow", "value": 70},
                                        {"color": "green", "value": 90}
                                    ]
                                }
                            }
                        },
                        "gridPos": {"h": 6, "w": 8, "x": 16, "y": 9}
                    }
                ],
                "time": {"from": "now-1h", "to": "now"},
                "refresh": "5s"
            }
        }
    
    def generate_metabase_questions(self) -> List[Dict[str, Any]]:
        """Gera perguntas/queries para Metabase"""
        return [
            {
                "name": "Node Performance Summary",
                "description": "Overview of all node performance metrics",
                "query": {
                    "type": "query",
                    "database": 1,
                    "query": {
                        "source-table": 1,
                        "aggregation": [["avg", ["field", "cpu_usage", None]]],
                        "breakout": [["field", "node_type", None]],
                        "filter": ["time-interval", ["field", "timestamp", None], -30, "day"]
                    }
                },
                "visualization_settings": {
                    "graph.dimensions": ["node_type"],
                    "graph.metrics": ["cpu_usage"]
                }
            },
            {
                "name": "Network Topology Analysis",
                "description": "Analysis of network connections and patterns",
                "query": {
                    "type": "native",
                    "database": 1,
                    "native": {
                        "query": """
                        SELECT 
                            source_node,
                            target_node,
                            COUNT(*) as connection_count,
                            AVG(connection_strength) as avg_strength
                        FROM network_connections 
                        WHERE timestamp >= NOW() - INTERVAL '24 hours'
                        GROUP BY source_node, target_node
                        ORDER BY connection_count DESC
                        LIMIT 50
                        """
                    }
                }
            },
            {
                "name": "Energy Consumption Trends",
                "description": "Energy usage patterns across the network",
                "query": {
                    "type": "query",
                    "database": 1,
                    "query": {
                        "source-table": 2,
                        "aggregation": [["sum", ["field", "energy_consumed", None]]],
                        "breakout": [
                            ["field", "node_type", None],
                            ["datetime-field", ["field", "timestamp", None], "day"]
                        ],
                        "filter": ["time-interval", ["field", "timestamp", None], -7, "day"]
                    }
                }
            }
        ]
    
    def create_qgis_project_template(self) -> Dict[str, Any]:
        """Cria template de projeto QGIS para dados geoespaciais"""
        return {
            "project_name": "AEONCOSMA Geospatial Analysis",
            "crs": "EPSG:4326",  # WGS84
            "layers": [
                {
                    "name": "Node Locations",
                    "type": "point",
                    "datasource": "postgresql://user:pass@localhost/aeoncosma",
                    "table": "node_locations",
                    "geometry_column": "geom",
                    "styling": {
                        "symbol": "circle",
                        "size_expression": "scale_linear(performance_score, 0, 100, 5, 20)",
                        "color_expression": "CASE WHEN node_type = 'master' THEN 'red' WHEN node_type = 'validator' THEN 'blue' ELSE 'green' END"
                    }
                },
                {
                    "name": "Network Connections",
                    "type": "line",
                    "datasource": "postgresql://user:pass@localhost/aeoncosma",
                    "table": "network_connections_geo",
                    "geometry_column": "geom",
                    "styling": {
                        "width_expression": "scale_linear(connection_strength, 0, 1, 1, 5)",
                        "color": "rgba(0, 255, 136, 0.7)"
                    }
                },
                {
                    "name": "Coverage Areas",
                    "type": "polygon",
                    "datasource": "postgresql://user:pass@localhost/aeoncosma", 
                    "table": "coverage_areas",
                    "geometry_column": "geom",
                    "styling": {
                        "fill_color": "rgba(74, 144, 226, 0.3)",
                        "stroke_color": "rgba(74, 144, 226, 0.8)"
                    }
                }
            ],
            "analysis_tools": [
                "Network Density Analysis",
                "Spatial Clustering", 
                "Coverage Optimization",
                "Nearest Neighbor Analysis"
            ]
        }
    
    def export_configurations(self, output_dir: str = "bi_configs"):
        """Exporta todas as configurações para arquivos"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Superset dashboard
        superset_config = self.generate_superset_dashboard_config()
        with open(output_path / "superset_dashboard.json", 'w') as f:
            json.dump(superset_config, f, indent=2)
        
        # Grafana dashboard
        grafana_config = self.generate_grafana_dashboard_json()
        with open(output_path / "grafana_dashboard.json", 'w') as f:
            json.dump(grafana_config, f, indent=2)
        
        # Metabase questions
        metabase_questions = self.generate_metabase_questions()
        with open(output_path / "metabase_questions.json", 'w') as f:
            json.dump(metabase_questions, f, indent=2)
        
        # QGIS project
        qgis_project = self.create_qgis_project_template()
        with open(output_path / "qgis_project_template.json", 'w') as f:
            json.dump(qgis_project, f, indent=2)
        
        print(f"✅ All BI configurations exported to {output_path}")
        
        return output_path

def main():
    """Demonstração da integração com BI platforms"""
    bi_integration = BIPlatformIntegration()
    
    print("🌟 AEONCOSMA BI Platform Integration")
    print("===================================")
    
    # Exportar configurações
    config_path = bi_integration.export_configurations()
    
    print(f"\n📁 Configuration files created in: {config_path}")
    print("\n🔧 Available integrations:")
    print("  • Apache Superset - Enterprise BI platform")
    print("  • Metabase - Simple business intelligence")
    print("  • Grafana - Monitoring and observability")
    print("  • QGIS - Geospatial analysis")
    
    print("\n🚀 Next steps:")
    print("  1. Set up your BI platform of choice")
    print("  2. Import the generated configuration files")
    print("  3. Configure database connections")
    print("  4. Start visualizing AEONCOSMA data!")

if __name__ == "__main__":
    main()
