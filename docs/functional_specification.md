# Saarthi - Role-Based Access Control (RBAC) and Functional Specification

## 1. Access Control Model
The system shall implement a Role-Based Access Control (RBAC) mechanism to enforce authorization boundaries across all system actors. Each authenticated user shall be associated with a predefined role, and access to system resources shall be governed via role-scoped permissions.

### 1.1 Defined Roles and Permission Scope

#### 1.1.1 Student Role
The Student entity shall have restricted access to onboarding and academic support functionalities, including:
- Retrieval of personalized onboarding checklist artifacts
- Submission of queries via conversational or ticketing interfaces
- Upload and lifecycle tracking of required documents
- Visibility into task state transitions (pending, in-progress, completed)
- Reception of system-generated notifications and reminders
- Access to adaptive guidance workflows
- Retrieval of assigned mentor metadata and institutional contact points

#### 1.1.2 Administrative Staff Role
The Administrative Staff role shall operate as a process executor and validator, with privileges including:
- Authoring and publishing onboarding requirement schemas
- Performing document validation (approve/reject workflows)
- Updating task states within onboarding pipelines
- Broadcasting system-wide or cohort-specific announcements
- Handling escalated or unresolved student queries
- Managing student group segmentation and cohort assignments

#### 1.1.3 Mentor / Faculty Advisor Role
The Mentor role shall function as a supervisory and advisory entity, with capabilities including:
- Accessing assigned student cohorts
- Monitoring onboarding completion metrics and progress states
- Delivering contextual academic or procedural guidance
- Tracking student engagement and progression signals
- Receiving escalation alerts for unresolved or critical issues

#### 1.1.4 System Administrator Role
The System Administrator shall have full control-plane access, including:
- Dynamic management of user roles and permission mappings
- Configuration of onboarding workflows and state machines
- Maintenance of system templates and reusable artifacts
- Control over global system configurations and feature toggles
- Monitoring of system logs, audit trails, and access control events

---

## 2. Functional Requirements Specification

### 2.1 Identity, Authentication, and Profile Management
The system shall:
- Support authentication via institutional credentials or unique registration identifiers
- Instantiate and persist a student profile entity post-authentication
- Maintain structured admission metadata (department, program, batch, residency status, onboarding phase)
- Enable controlled profile updates with validation and verification layers

### 2.2 Dynamic Onboarding Checklist Engine
The system shall implement a rule-driven checklist generation engine that:
- Produces personalized onboarding task sets based on student attributes
- Maintains task lifecycle states (pending, in-progress, completed)
- Dynamically adapts checklist composition based on contextual parameters (department, hostel allocation, fee status, document verification)
- Prioritizes tasks using deadline-driven and rule-based ordering

### 2.3 Intelligent Guidance and Query Resolution Agent
The system shall provide an AI-assisted guidance layer capable of:
- Resolving standard onboarding queries via NLP-driven interfaces
- Delivering procedural instructions in a stepwise manner
- Recommending next-best actions based on user state context
- Handling domain-specific queries (documents, LMS, timetable, hostel, fees)
- Escalating unresolved queries to human operators via ticketing workflows

### 2.4 Document Management and Verification Pipeline
The system shall implement a document ingestion and validation pipeline that:
- Supports secure document upload with format and integrity validation
- Maps documents to predefined requirement categories
- Maintains document states (pending review, approved, rejected)
- Triggers feedback loops for rejected or incomplete submissions
- Enables administrative review and approval workflows

### 2.5 Financial Tracking and Fee Management
The system shall:
- Integrate with payment systems to reflect real-time fee status
- Display outstanding dues and payment confirmations
- Generate automated reminders for unpaid obligations
- Support manual proof-of-payment submission for offline verification

### 2.6 Course Registration Assistance Module
The system shall:
- Provide structured guidance for course registration processes
- Surface deadlines and eligibility constraints
- Present course catalogs (mandatory and elective)
- Detect and flag incomplete or failed registrations

### 2.7 Academic Schedule and Timetable Management
The system shall:
- Provide access to class schedules and orientation events
- Maintain onboarding-critical deadlines
- Notify users of timetable updates
- Persist academic calendar data relevant to onboarding cohorts

### 2.8 Learning Management System (LMS) Integration
The system shall:
- Guide first-time LMS access and configuration
- Map users to assigned courses/modules
- Detect access anomalies and provide remediation steps
- Notify users of incomplete LMS onboarding

### 2.9 Hostel Allocation Workflow Support
The system shall:
- Track hostel application and allocation status
- Manage hostel-specific documentation requirements
- Provide allocation outcomes and check-in instructions
- Guide users through hostel onboarding workflows

### 2.10 Mentor Assignment and Communication Layer
The system shall:
- Map students to mentors via configurable assignment logic
- Provide mentor metadata visibility
- Enable structured communication (chat/ticket-based)
- Support escalation pipelines and response tracking

### 2.11 Compliance and Induction Tracking
The system shall:
- Maintain a registry of mandatory compliance modules
- Track completion status and certification records
- Generate reminders for pending compliance tasks
- Alert administrators on non-compliance

### 2.12 Notification and Eventing System
The system shall:
- Support multi-channel notifications (email, SMS, in-app)
- Trigger reminders based on deadlines and system events
- Notify users of approval/rejection events
- Allow configurable scheduling and notification policies

### 2.13 Knowledge Base and FAQ System
The system shall:
- Provide a searchable, categorized knowledge repository
- Enable dynamic FAQ management by administrators
- Deliver context-aware content recommendations

### 2.14 Escalation and Ticketing System
The system shall:
- Generate support tickets for unresolved issues
- Classify tickets based on domain and priority
- Route tickets to appropriate departments
- Track lifecycle and status of each ticket
- Notify users of updates and resolutions

### 2.15 Administrative Dashboard and Analytics
The system shall provide a centralized observability layer including:
- Aggregate onboarding progress metrics
- Pending approval queues
- Ticket backlog visibility
- Document verification workload insights
- Completion analytics segmented by cohort (batch, department)
- Filtering and reporting capabilities

### 2.16 Audit Logging and Compliance Tracking
The system shall implement a comprehensive audit framework that:
- Logs all user and administrative actions
- Captures state transitions (approvals, rejections, updates)
- Stores timestamped event records
- Maintains immutable audit trails for compliance and traceability
