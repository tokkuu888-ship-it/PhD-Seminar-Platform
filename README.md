# PhD Seminar Platform

A comprehensive Flask web application for managing PhD seminars, progress monitoring, and academic collaboration based on the PhD Seminar and Progress Monitoring Blueprint.

## Features

### Core Objectives
- **Timely Completion**: Establish accountability to keep students on dissertation timelines
- **Defense Readiness**: Build rhetorical confidence through simulated viva sessions
- **Professional Socialization**: Foster a community of practice between faculty and students

### Key Features
- **Adaptive Scheduling**: Bi-weekly windows with availability polls for busy professors
- **4-Phase Seminar Format**: 
  - Presentation (30 min)
  - Peer Review (15 min) 
  - Faculty Viva (30 min)
  - Mentorship (15 min)
- **Progress Monitoring**: One-page progress reports for efficient faculty preparation
- **Hybrid Flexibility**: Remote participation support with video conferencing integration
- **Role-Based Access**: Dean, Professor, and PhD Candidate roles with appropriate permissions
- **Responsive Design**: Mobile and desktop compatible interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- ngrok account and authtoken

### Setup Instructions

1. **Clone or download the project files to your directory**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure ngrok:**
   - Get your authtoken from your ngrok dashboard
   - Update the `.env` file with your authtoken:
     ```
     NGROK_AUTHTOKEN=your_actual_authtoken_here
     ```
   - Alternatively, update the authtoken directly in `app.py`:
     ```python
     NGROK_AUTHTOKEN = "your_actual_authtoken_here"
     ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the platform:**
   - Local: http://localhost:5000
   - Remote: Use the ngrok URL provided in the console output

## Demo Accounts

The platform creates default demo accounts for testing:

| Role | Username | Password |
|------|----------|----------|
| Dean | dean | admin123 |
| Professor | professor1 | prof123 |
| PhD Candidate | student1 | student123 |

## Platform Architecture

### User Roles
- **Dean**: High-level oversight, schedule approval
- **Professor**: Schedule seminars, provide faculty feedback, manage availability
- **PhD Candidate**: Submit progress reports, present seminars, provide peer feedback

### Database Models
- **User**: Authentication and role management
- **Seminar**: Seminar scheduling and management
- **Availability**: Faculty availability tracking
- **ProgressReport**: Student progress submissions
- **Feedback**: Peer and faculty feedback system

### Key Features Implementation

#### Seminar Scheduling System
- Flexible bi-weekly scheduling windows
- Availability polls for faculty coordination
- Hybrid meeting support with video conferencing links
- 90-minute session duration with structured phases

#### Progress Monitoring
- One-page progress reports submitted before seminars
- Structured sections for achievements, challenges, and next steps
- Word count guidance and validation
- Faculty preparation optimization

#### Feedback System
- **Peer Review**: Supportive feedback from fellow PhD candidates
- **Faculty Viva**: Professional feedback using Sandwich Method
- Rating system for faculty evaluations
- Constructive, actionable feedback guidelines

#### Responsive Design
- Bootstrap 5 framework for mobile compatibility
- Touch-friendly interface for tablets and smartphones
- Progressive enhancement for different screen sizes
- Accessible design following WCAG guidelines

## Remote Access Configuration

The platform uses ngrok for secure remote access:

1. **Authentication**: Configure your ngrok authtoken in `.env` or `app.py`
2. **Automatic Tunnel**: The app automatically creates an ngrok tunnel on startup
3. **Secure URL**: Get your public URL from the console output
4. **Share Access**: Distribute the ngrok URL to remote participants

## Security Considerations

- Password hashing with Werkzeug security
- Role-based access control
- Session management with Flask-Login
- Input validation and sanitization
- Secure ngrok tunneling for remote access

## Development Notes

### Database
- SQLite database for simplicity and portability
- SQLAlchemy ORM for database operations
- Automatic table creation on first run

### Frontend
- Bootstrap 5 for responsive design
- Font Awesome icons for visual consistency
- Custom CSS for platform branding
- JavaScript for interactive features

### Backend
- Flask framework for web application
- Flask-Login for authentication
- Flask-SQLAlchemy for database management
- pyngrok for remote access tunneling

## Troubleshooting

### Common Issues

1. **Ngrok Authentication Failed**
   - Verify your authtoken is correct
   - Check internet connection
   - Ensure ngrok account is active

2. **Database Errors**
   - Delete `phd_seminar.db` to reset database
   - Restart application to recreate tables

3. **Port Conflicts**
   - Change port in `app.py` if 5000 is in use
   - Update ngrok configuration accordingly

### Support

For technical support or feature requests, refer to the platform documentation or contact your system administrator.

## Future Enhancements

- Email notifications for seminar reminders
- File upload support for presentation materials
- Advanced analytics and reporting
- Integration with university calendar systems
- Multi-language support
- Video conferencing integration (Zoom, Teams, Google Meet)

---

**© 2026 PhD Seminar Platform. Supporting doctoral excellence through structured seminars and collaborative progress monitoring.**
