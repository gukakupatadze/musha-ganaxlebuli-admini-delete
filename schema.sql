-- DataLab Georgia PostgreSQL Schema
-- Created for MongoDB to PostgreSQL migration

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Service Requests Table
CREATE TABLE service_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    device_type VARCHAR(50) NOT NULL CHECK (device_type IN ('hdd', 'ssd', 'raid', 'usb', 'sd', 'other')),
    problem_description TEXT NOT NULL,
    urgency VARCHAR(20) NOT NULL CHECK (urgency IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'picked_up', 'archived')),
    case_id VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    estimated_completion TIMESTAMP WITH TIME ZONE,
    price DECIMAL(10,2),
    is_read BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    approved_for_kanban BOOLEAN DEFAULT FALSE,
    admin_comment TEXT
);

-- Contact Messages Table
CREATE TABLE contact_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'read', 'replied'))
);

-- Testimonials Table
CREATE TABLE testimonials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    position_en VARCHAR(100) NOT NULL,
    text_ka TEXT NOT NULL,
    text_en TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5) DEFAULT 5,
    image VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Price Estimates Table (optional - for storing price calculation history)
CREATE TABLE price_estimates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_type VARCHAR(50) NOT NULL,
    problem_type VARCHAR(50) NOT NULL,
    urgency VARCHAR(20) NOT NULL,
    estimated_price DECIMAL(10,2) NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET
);

-- Indexes for performance
CREATE INDEX idx_service_requests_case_id ON service_requests(case_id);
CREATE INDEX idx_service_requests_email ON service_requests(email);
CREATE INDEX idx_service_requests_status ON service_requests(status);
CREATE INDEX idx_service_requests_created_at ON service_requests(created_at DESC);
CREATE INDEX idx_service_requests_approved_kanban ON service_requests(approved_for_kanban) WHERE approved_for_kanban = TRUE;

CREATE INDEX idx_contact_messages_email ON contact_messages(email);
CREATE INDEX idx_contact_messages_status ON contact_messages(status);
CREATE INDEX idx_contact_messages_created_at ON contact_messages(created_at DESC);

CREATE INDEX idx_testimonials_active ON testimonials(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_testimonials_rating ON testimonials(rating DESC);

-- Triggers for case_id generation (similar to MongoDB sequence)
CREATE SEQUENCE case_id_seq START 1;

CREATE OR REPLACE FUNCTION generate_case_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.case_id IS NULL OR NEW.case_id = '' THEN
        NEW.case_id := 'DL' || EXTRACT(YEAR FROM NOW()) || LPAD(nextval('case_id_seq')::text, 3, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_generate_case_id
    BEFORE INSERT ON service_requests
    FOR EACH ROW
    EXECUTE FUNCTION generate_case_id();

-- Grant permissions to datalab_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO datalab_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO datalab_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO datalab_user;