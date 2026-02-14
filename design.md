# Design Document: Bharat Exam Buddy

## Overview

Bharat Exam Buddy is a Python-based web application that provides AI-powered educational assistance to Indian students. The system uses Streamlit for the user interface and integrates with Amazon Bedrock to access foundation models (Claude, Titan) for generating simplified explanations of complex academic concepts.

The architecture follows a layered approach:
- **Presentation Layer**: Streamlit UI for user interaction
- **Business Logic Layer**: Question processing, response formatting, and configuration management
- **Integration Layer**: Amazon Bedrock client for AI model inference
- **Fallback Layer**: Mock response system for demo/testing purposes

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Question     │  │ Submit       │  │ Response     │      │
│  │ Input Area   │  │ Button       │  │ Display      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Logic Layer                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Question Validator                                   │   │
│  │  - Validate input                                     │   │
│  │  - Sanitize text                                      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Response Formatter                                   │   │
│  │  - Format markdown                                    │   │
│  │  - Structure output                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Configuration Manager                                │   │
│  │  - Mode selection (Bedrock/Mock)                      │   │
│  │  - Environment settings                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Bedrock Client         │  │   Mock Response          │
│   - boto3 integration    │  │   - Demo responses       │
│   - API calls            │  │   - Pattern matching     │
│   - Error handling       │  │                          │
└──────────────────────────┘  └──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────────────────────┐
│              Amazon Bedrock Service                       │
│  ┌────────────────┐         ┌────────────────┐          │
│  │ Claude Model   │         │ Titan Model    │          │
│  └────────────────┘         └────────────────┘          │
└──────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. User enters question in Streamlit UI
2. Question Validator checks input validity
3. Configuration Manager determines mode (Bedrock/Mock)
4. If Bedrock mode:
   - Bedrock Client sends request to AWS Bedrock
   - Foundation model generates response
   - Response returned to application
5. If Mock mode:
   - Mock Response system generates demo response
6. Response Formatter structures the output
7. Streamlit UI displays formatted explanation

## Components and Interfaces

### 1. Question Validator

**Purpose**: Validate and sanitize user input before processing

**Interface**:
```python
class QuestionValidator:
    def validate(question: str) -> ValidationResult:
        """
        Validates a question string.
        
        Args:
            question: The user's input question
            
        Returns:
            ValidationResult with is_valid flag and error message if invalid
        """
        pass
    
    def sanitize(question: str) -> str:
        """
        Sanitizes question text by removing excessive whitespace
        and normalizing formatting.
        
        Args:
            question: Raw question text
            
        Returns:
            Sanitized question string
        """
        pass
```

**Validation Rules**:
- Question must not be empty or only whitespace
- Question length should be reasonable (e.g., 1-2000 characters)
- Strip leading/trailing whitespace
- Normalize multiple spaces to single space

### 2. Bedrock Client

**Purpose**: Handle communication with Amazon Bedrock API

**Interface**:
```python
class BedrockClient:
    def __init__(region_name: str, model_id: str):
        """
        Initialize Bedrock client.
        
        Args:
            region_name: AWS region (e.g., 'us-east-1')
            model_id: Foundation model identifier (e.g., 'anthropic.claude-v2')
        """
        pass
    
    def generate_explanation(question: str, max_tokens: int = 500) -> BedrockResponse:
        """
        Generate an explanation for the given question.
        
        Args:
            question: The validated question
            max_tokens: Maximum tokens in response
            
        Returns:
            BedrockResponse containing the explanation or error
            
        Raises:
            BedrockAPIError: If API call fails
            AuthenticationError: If credentials are invalid
        """
        pass
```

**Implementation Details**:
- Use boto3 client for 'bedrock-runtime' service
- Construct JSON request body with prompt and parameters
- Handle API response parsing
- Implement retry logic for transient failures
- Proper error handling and logging

### 3. Mock Response System

**Purpose**: Provide demo responses when Bedrock is not available

**Interface**:
```python
class MockResponseSystem:
    def generate_explanation(question: str) -> str:
        """
        Generate a mock explanation based on question keywords.
        
        Args:
            question: The user's question
            
        Returns:
            Formatted mock explanation string
        """
        pass
    
    def add_response_pattern(keywords: List[str], response: str):
        """
        Add a new pattern-response mapping for demo mode.
        
        Args:
            keywords: List of keywords to match
            response: Response template to return
        """
        pass
```

**Pattern Matching Strategy**:
- Maintain dictionary of keyword patterns to responses
- Case-insensitive keyword matching
- Support multiple keywords per response
- Default fallback response for unmatched questions

### 4. Response Formatter

**Purpose**: Format AI responses into structured, readable markdown

**Interface**:
```python
class ResponseFormatter:
    def format_explanation(question: str, raw_response: str, mode: str) -> str:
        """
        Format the AI response into structured markdown.
        
        Args:
            question: Original user question
            raw_response: Raw response from AI or mock system
            mode: 'bedrock' or 'mock' to indicate source
            
        Returns:
            Formatted markdown string ready for display
        """
        pass
    
    def add_metadata(formatted_response: str, metadata: Dict) -> str:
        """
        Add metadata footer to response (e.g., model info, timestamp).
        
        Args:
            formatted_response: Already formatted response
            metadata: Dictionary of metadata to include
            
        Returns:
            Response with metadata footer
        """
        pass
```

**Formatting Rules**:
- Add heading for "Simple Explanation"
- Display original question prominently
- Preserve markdown from AI response (headings, lists, bold, italic)
- Add visual separators between sections
- Include footer with mode indicator

### 5. Configuration Manager

**Purpose**: Manage application configuration and mode selection

**Interface**:
```python
class ConfigurationManager:
    def __init__(config_file: Optional[str] = None):
        """
        Initialize configuration from file or environment.
        
        Args:
            config_file: Optional path to configuration file
        """
        pass
    
    def is_bedrock_enabled() -> bool:
        """Returns True if Bedrock mode is enabled."""
        pass
    
    def get_bedrock_config() -> BedrockConfig:
        """
        Get Bedrock configuration parameters.
        
        Returns:
            BedrockConfig with region, model_id, max_tokens
        """
        pass
    
    def get_aws_credentials() -> AWSCredentials:
        """
        Get AWS credentials from environment or credential chain.
        
        Returns:
            AWSCredentials object or None if using IAM role
        """
        pass
```

**Configuration Sources** (in priority order):
1. Environment variables
2. Configuration file (.env or config.json)
3. Default values

**Key Configuration Parameters**:
- `USE_BEDROCK`: Boolean flag for mode selection
- `AWS_REGION`: AWS region for Bedrock (default: 'us-east-1')
- `MODEL_ID`: Foundation model identifier (default: 'anthropic.claude-v2')
- `MAX_TOKENS`: Maximum response length (default: 500)

### 6. Streamlit UI Controller

**Purpose**: Orchestrate UI components and user interactions

**Interface**:
```python
class StreamlitUIController:
    def __init__(config_manager: ConfigurationManager):
        """
        Initialize UI controller with configuration.
        
        Args:
            config_manager: Configuration manager instance
        """
        pass
    
    def render_ui():
        """Render the complete Streamlit interface."""
        pass
    
    def handle_question_submission(question: str):
        """
        Handle question submission and display response.
        
        Args:
            question: User's submitted question
        """
        pass
    
    def display_error(error_message: str):
        """
        Display error message to user.
        
        Args:
            error_message: User-friendly error description
        """
        pass
```

## Data Models

### ValidationResult

```python
@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
    sanitized_question: Optional[str] = None
```

### BedrockResponse

```python
@dataclass
class BedrockResponse:
    success: bool
    explanation: Optional[str] = None
    error: Optional[str] = None
    model_id: str = ""
    tokens_used: int = 0
```

### BedrockConfig

```python
@dataclass
class BedrockConfig:
    region_name: str = "us-east-1"
    model_id: str = "anthropic.claude-v2"
    max_tokens: int = 500
    temperature: float = 0.7
```

### AWSCredentials

```python
@dataclass
class AWSCredentials:
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    session_token: Optional[str] = None
    # None values indicate using IAM role or credential chain
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Input Validation Rejects Empty Questions

*For any* string composed entirely of whitespace characters (spaces, tabs, newlines) or empty string, the validation system should reject it and return an error message.

**Validates: Requirements 1.3**

### Property 2: Question Appears in Formatted Response

*For any* valid question and any response (mock or Bedrock), the formatted output should contain the original question text.

**Validates: Requirements 1.4, 2.4**

### Property 3: Response Formatting Preserves Structure

*For any* AI response containing markdown elements (headings, lists, bold, italics, code blocks), the formatting system should preserve all markdown syntax in the final output.

**Validates: Requirements 2.3, 2.5, 5.1, 5.2, 5.3, 5.5**

### Property 4: API Request Construction

*For any* valid question, when Bedrock mode is enabled, the API request should include all required parameters: model_id, prompt (containing the question), max_tokens, and the client should be configured with the correct AWS region.

**Validates: Requirements 3.2, 3.3, 3.4**

### Property 5: JSON Response Parsing Round-Trip

*For any* valid Bedrock API response structure, parsing the JSON response should correctly extract the explanation text without data loss.

**Validates: Requirements 3.5**

### Property 6: Fallback Mode Activation

*For any* question, when Bedrock API calls fail or Bedrock is disabled, the system should successfully generate a response using the mock system without crashing.

**Validates: Requirements 3.6, 6.2**

### Property 7: Error Handling Without Crashes

*For any* error condition (API failure, malformed response, network error, invalid credentials), the system should handle the error gracefully, display a user-friendly message, and continue functioning for subsequent requests.

**Validates: Requirements 4.1, 4.2, 4.3, 4.5**

### Property 8: Error Logging Completeness

*For any* error that occurs during processing, the system should create a log entry containing sufficient context (error type, timestamp, relevant parameters) for debugging.

**Validates: Requirements 4.4**

### Property 9: Configuration-Based Mode Routing

*For any* question, the system should route to Bedrock client when USE_BEDROCK is True, and route to mock system when USE_BEDROCK is False, with the configuration clearly indicating the active mode.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

### Property 10: Mock Response Quality

*For any* question processed in mock mode, the generated response should be non-empty, properly formatted as markdown, and contain relevant content based on keyword matching.

**Validates: Requirements 6.5**

### Property 11: AWS Credential Chain Support

*For any* valid AWS credential source (environment variables, IAM role, credential file), the boto3 client should successfully authenticate with Bedrock using the standard credential resolution chain.

**Validates: Requirements 8.1, 8.2**

### Property 12: Credential Error Messaging

*For any* invalid or missing AWS credentials, the system should detect the authentication failure and display a clear, actionable error message to the user.

**Validates: Requirements 8.4**

## Error Handling

### Error Categories

1. **Validation Errors**
   - Empty or invalid question input
   - Question exceeds maximum length
   - **Handling**: Display validation message, do not process request

2. **API Errors**
   - Bedrock API call failure (5xx errors)
   - Rate limiting (429 errors)
   - **Handling**: Log error, display user-friendly message, optionally retry with exponential backoff

3. **Authentication Errors**
   - Invalid AWS credentials
   - Insufficient IAM permissions
   - **Handling**: Log error with details, display clear message about credential configuration

4. **Network Errors**
   - Connection timeout
   - DNS resolution failure
   - **Handling**: Log error, display connectivity message, suggest checking network

5. **Parsing Errors**
   - Malformed JSON response
   - Unexpected response structure
   - **Handling**: Log raw response, display generic error message, continue operation

6. **Configuration Errors**
   - Invalid model ID
   - Missing required configuration
   - **Handling**: Fail fast on startup with clear error message

### Error Response Format

All errors should be communicated to users through Streamlit's warning/error components:

```python
# Validation errors
st.warning("Please enter a question.")

# API errors
st.error("Unable to generate explanation. Please try again.")

# Authentication errors
st.error("AWS credentials not configured. Please check your AWS setup.")

# Network errors
st.error("Connection error. Please check your internet connection.")
```

### Logging Strategy

Use Python's logging module with appropriate levels:

- **DEBUG**: Detailed information for diagnosing problems (API request/response bodies)
- **INFO**: General informational messages (mode selection, successful operations)
- **WARNING**: Warning messages for recoverable issues (fallback activation)
- **ERROR**: Error messages for failures (API errors, parsing errors)
- **CRITICAL**: Critical errors that prevent application startup (configuration errors)

Example logging:
```python
logger.info(f"Processing question in {'Bedrock' if use_bedrock else 'Mock'} mode")
logger.error(f"Bedrock API call failed: {error_message}", exc_info=True)
logger.warning("Falling back to mock response system")
```

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and integration points
- **Property-based tests**: Verify universal properties across randomized inputs

Both approaches are complementary and necessary for thorough validation.

### Property-Based Testing

**Library**: Use `hypothesis` for Python property-based testing

**Configuration**:
- Minimum 100 iterations per property test
- Each test must reference its design document property using a comment tag
- Tag format: `# Feature: bharat-exam-buddy, Property {number}: {property_text}`

**Property Test Examples**:

```python
from hypothesis import given, strategies as st
import pytest

# Feature: bharat-exam-buddy, Property 1: Input Validation Rejects Empty Questions
@given(st.text().filter(lambda s: s.strip() == ""))
def test_empty_question_validation(empty_question):
    """Property: Empty/whitespace questions should be rejected."""
    validator = QuestionValidator()
    result = validator.validate(empty_question)
    assert not result.is_valid
    assert result.error_message is not None

# Feature: bharat-exam-buddy, Property 2: Question Appears in Formatted Response
@given(st.text(min_size=1, max_size=500))
def test_question_in_response(question):
    """Property: Original question should appear in formatted output."""
    formatter = ResponseFormatter()
    response = "This is a test explanation."
    formatted = formatter.format_explanation(question, response, "mock")
    assert question in formatted

# Feature: bharat-exam-buddy, Property 9: Configuration-Based Mode Routing
@given(st.booleans(), st.text(min_size=1, max_size=100))
def test_mode_routing(use_bedrock, question):
    """Property: System should route based on configuration flag."""
    config = ConfigurationManager()
    config.set_bedrock_enabled(use_bedrock)
    
    # Mock both systems and verify correct one is called
    with patch('bedrock_client.generate') as mock_bedrock, \
         patch('mock_system.generate') as mock_mock:
        
        controller = StreamlitUIController(config)
        controller.handle_question_submission(question)
        
        if use_bedrock:
            mock_bedrock.assert_called_once()
            mock_mock.assert_not_called()
        else:
            mock_mock.assert_called_once()
            mock_bedrock.assert_not_called()
```

### Unit Testing

**Framework**: Use `pytest` for unit testing

**Focus Areas**:
1. **Specific Examples**: Test known question-response pairs
2. **Edge Cases**: Test boundary conditions (max length, special characters)
3. **Error Conditions**: Test specific error scenarios
4. **Integration Points**: Test component interactions

**Unit Test Examples**:

```python
def test_dna_question_mock_response():
    """Test specific DNA question gets appropriate mock response."""
    mock_system = MockResponseSystem()
    response = mock_system.generate_explanation("What is DNA?")
    assert "genetic information" in response.lower()
    assert "molecule" in response.lower()

def test_bedrock_client_initialization():
    """Test Bedrock client initializes with correct parameters."""
    client = BedrockClient(region_name="us-east-1", model_id="anthropic.claude-v2")
    assert client.region_name == "us-east-1"
    assert client.model_id == "anthropic.claude-v2"

def test_api_error_handling():
    """Test specific API error produces user-friendly message."""
    with patch('boto3.client') as mock_boto:
        mock_boto.return_value.invoke_model.side_effect = ClientError(
            {'Error': {'Code': '500', 'Message': 'Internal Server Error'}},
            'invoke_model'
        )
        
        client = BedrockClient("us-east-1", "anthropic.claude-v2")
        response = client.generate_explanation("Test question")
        
        assert not response.success
        assert "error" in response.error.lower()

def test_markdown_preservation():
    """Test that specific markdown elements are preserved."""
    formatter = ResponseFormatter()
    response_with_markdown = "# Heading\n\n**Bold text**\n\n- List item"
    formatted = formatter.format_explanation("Test?", response_with_markdown, "mock")
    
    assert "# Heading" in formatted
    assert "**Bold text**" in formatted
    assert "- List item" in formatted

def test_no_hardcoded_credentials():
    """Test that source code doesn't contain hardcoded AWS credentials."""
    with open("app.py", "r") as f:
        content = f.read()
    
    # Check for common patterns of hardcoded credentials
    assert "AKIA" not in content  # AWS access key prefix
    assert "aws_access_key_id" not in content or "aws_access_key_id=" not in content
    assert "aws_secret_access_key" not in content or "aws_secret_access_key=" not in content
```

### Test Coverage Goals

- **Line Coverage**: Minimum 80% for all modules
- **Branch Coverage**: Minimum 75% for conditional logic
- **Property Coverage**: 100% of design properties must have corresponding property tests
- **Critical Path Coverage**: 100% for question submission and response generation flows

### Testing Execution

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Run only property tests
pytest -m property tests/

# Run only unit tests
pytest -m unit tests/

# Run with hypothesis verbosity
pytest --hypothesis-verbosity=verbose tests/
```

### Continuous Integration

Tests should be executed automatically on:
- Every commit to feature branches
- Pull requests to main branch
- Scheduled daily runs with extended property test iterations (1000+ per property)

## Implementation Notes

### Technology Stack

- **Python 3.9+**: Core language
- **Streamlit**: Web UI framework
- **boto3**: AWS SDK for Bedrock integration
- **hypothesis**: Property-based testing library
- **pytest**: Unit testing framework
- **python-dotenv**: Environment variable management (optional)

### Dependencies

```
streamlit>=1.28.0
boto3>=1.28.0
hypothesis>=6.82.0
pytest>=7.4.0
pytest-cov>=4.1.0
python-dotenv>=1.0.0
```

### File Structure

```
bharat-exam-buddy/
├── app.py                          # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── validators.py               # QuestionValidator
│   ├── bedrock_client.py           # BedrockClient
│   ├── mock_system.py              # MockResponseSystem
│   ├── formatters.py               # ResponseFormatter
│   ├── config.py                   # ConfigurationManager
│   └── ui_controller.py            # StreamlitUIController
├── tests/
│   ├── __init__.py
│   ├── test_validators.py          # Validator tests
│   ├── test_bedrock_client.py      # Bedrock client tests
│   ├── test_mock_system.py         # Mock system tests
│   ├── test_formatters.py          # Formatter tests
│   ├── test_config.py              # Configuration tests
│   ├── test_integration.py         # Integration tests
│   └── property_tests/
│       ├── __init__.py
│       ├── test_properties_validation.py
│       ├── test_properties_formatting.py
│       ├── test_properties_api.py
│       └── test_properties_config.py
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── .env.example                    # Example environment configuration
├── pytest.ini                      # Pytest configuration
└── README.md                       # Project documentation
```

### Environment Configuration

Create a `.env` file for local development:

```
USE_BEDROCK=false
AWS_REGION=us-east-1
MODEL_ID=anthropic.claude-v2
MAX_TOKENS=500
LOG_LEVEL=INFO
```

For production with Bedrock:

```
USE_BEDROCK=true
AWS_REGION=us-east-1
MODEL_ID=anthropic.claude-v2
MAX_TOKENS=500
LOG_LEVEL=WARNING
```

### AWS IAM Permissions

The application requires the following IAM permissions for Bedrock access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:model/anthropic.claude-v2",
        "arn:aws:bedrock:*:*:model/amazon.titan-*"
      ]
    }
  ]
}
```

### Deployment Considerations

1. **Local Development**: Use mock mode (USE_BEDROCK=false) to avoid AWS costs
2. **Staging**: Use Bedrock with lower max_tokens for cost control
3. **Production**: Use Bedrock with appropriate rate limiting and monitoring
4. **AWS Lambda**: Can be deployed as Lambda function with API Gateway (requires adaptation)
5. **Container**: Can be containerized with Docker for cloud deployment

### Security Best Practices

1. Never commit `.env` files or AWS credentials to version control
2. Use IAM roles when deploying to AWS services (EC2, Lambda, ECS)
3. Implement rate limiting to prevent abuse
4. Validate and sanitize all user inputs
5. Use HTTPS for all external communications
6. Regularly rotate AWS credentials
7. Monitor CloudWatch logs for suspicious activity
8. Implement request logging for audit trails
