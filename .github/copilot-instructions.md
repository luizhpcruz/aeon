# IA P2P Trader - Sistema Proprietário de Trading
<!-- Desenvolvido por Luiz - Todos os direitos reservados -->

## Visão do Projeto
Sistema de trading P2P com inteligência artificial proprietário que combina:
- **FastAPI backend** for trading APIs and data processing
- **React frontend** with modern UI/UX for trading interface
- **P2P networking** for decentralized trading
- **AI/ML models** for market analysis and predictions
- **Fractal analysis** for pattern recognition in financial data

## Code Style Guidelines
- Use **Python 3.9+** with type hints
- Follow **PEP 8** standards
- Use **async/await** for FastAPI endpoints
- Implement **proper error handling** and logging
- Use **Pydantic** models for data validation
- Write **comprehensive docstrings**

## Architecture Patterns
- **Clean Architecture** with separation of concerns
- **Repository pattern** for data access
- **Dependency injection** for services
- **Event-driven architecture** for P2P communication
- **Microservices** approach for scalability

## Security Considerations
- Implement **JWT authentication**
- Use **HTTPS** for all communications
- Validate **all inputs** and sanitize data
- Implement **rate limiting** and DDoS protection
- Use **secure P2P protocols**

## P2P Network Guidelines
When working with P2P code (especially p2p_node.py):
- Always use **proper exception handling** for network operations
- Implement **timeout mechanisms** for socket connections
- Use **threading** for concurrent client handling
- Add **peer discovery** mechanisms for network resilience
- Include **message validation** and **serialization safety**
- Implement **graceful shutdown** procedures
- Add **logging** for debugging network issues
- Use **socket options** like SO_REUSEADDR for robustness

## P2P Node Implementation Best Practices
- **Socket Management**: Always close connections in finally blocks
- **Threading Safety**: Use thread-safe data structures for peer lists
- **Message Protocol**: Define structured message formats with versioning
- **Error Recovery**: Implement retry mechanisms for failed connections
- **Network Topology**: Support multiple peer discovery methods
- **Data Persistence**: Consider saving peer information across restarts
- **Performance**: Use connection pooling for frequent communications

## AI/ML Guidelines
- Use **scikit-learn** for traditional ML models
- Consider **TensorFlow/PyTorch** for deep learning
- Implement **real-time prediction** pipelines
- Use **proper data preprocessing** and feature engineering
- Include **model versioning** and A/B testing

## Fractal Analysis Guidelines
- Implement **Box Counting** algorithm for fractal dimension
- Use **Hurst exponent** calculation for trend analysis
- Include **self-similarity** detection in price patterns
- Implement **multi-scale** analysis for different timeframes
- Use **detrended fluctuation analysis** for long-range correlations

## Frontend Guidelines
- Use **React 18+** with hooks
- Implement **TypeScript** for type safety
- Use **Tailwind CSS** for styling
- Follow **responsive design** principles
- Implement **real-time updates** with WebSockets

## Testing Strategy
- Write **unit tests** with pytest
- Implement **integration tests** for APIs
- Use **mock data** for P2P testing
- Include **performance tests** for trading algorithms
- Implement **end-to-end tests** for critical workflows

## File Structure Context
- `app/` - Core application logic with fractal analysis
- `ai-core/` - Machine learning models and predictors
- `backend/` - FastAPI server and REST APIs
- `frontend/` - React web application
- `p2p/` - Peer-to-peer networking components
- `p2p-network/` - Advanced P2P network implementation
- `data/` - Data storage and market data files
- `docs/` - Documentation and guides

## Specific Module Guidelines

### For p2p_node.py improvements:
- Add connection timeouts and retry logic
- Implement peer discovery and heartbeat mechanisms
- Use structured message formats with validation
- Add comprehensive error handling and logging
- Implement graceful shutdown and cleanup
- Support multiple concurrent connections efficiently
- Add network statistics and monitoring

### For fractal analysis modules:
- Ensure numerical stability in calculations
- Implement efficient algorithms for large datasets
- Add visualization capabilities for patterns
- Include confidence intervals in predictions
- Support multiple fractal analysis methods

### For trading AI components:
- Implement proper feature engineering pipelines
- Add model performance monitoring
- Include backtesting capabilities
- Support multiple prediction horizons
- Implement ensemble methods for robustness

## Development Workflow
- Use **start.py** as the main entry point for all services
- Support both **development** and **production** configurations
- Implement **hot reloading** for development
- Use **Docker** for deployment consistency
- Include **health checks** for all services

## Integration Points
- P2P nodes should integrate with fractal analysis engine
- Trading signals should be shared across the P2P network
- Web frontend should display real-time P2P network status
- All components should support graceful degradation when services are unavailable
