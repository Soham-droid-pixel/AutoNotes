const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const FLASK_ML_URL = process.env.FLASK_ML_URL || 'http://localhost:5001';

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' })); // Allow larger text inputs
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'AutoNotes Backend',
        timestamp: new Date().toISOString()
    });
});

// Main summarization endpoint
app.post('/api/summarize', async (req, res) => {
    try {
        const { text } = req.body;

        // Validate input
        if (!text) {
            return res.status(400).json({
                error: 'Missing text field in request body',
                status: 'error'
            });
        }

        if (typeof text !== 'string') {
            return res.status(400).json({
                error: 'Text must be a string',
                status: 'error'
            });
        }

        const trimmedText = text.trim();
        
        if (!trimmedText) {
            return res.status(400).json({
                error: 'Text cannot be empty',
                status: 'error'
            });
        }

        if (trimmedText.length < 50) {
            return res.status(400).json({
                error: 'Text too short. Please provide at least 50 characters.',
                status: 'error'
            });
        }

        if (trimmedText.length > 50000) {
            return res.status(400).json({
                error: 'Text too long. Please provide less than 50,000 characters.',
                status: 'error'
            });
        }

        console.log(`Processing text summarization request (${trimmedText.length} characters)`);

        // Make request to Flask ML service
        const mlResponse = await axios.post(`${FLASK_ML_URL}/summarize`, {
            text: trimmedText
        }, {
            timeout: 30000, // 30 second timeout
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Validate ML service response
        if (!mlResponse.data || !mlResponse.data.summary) {
            throw new Error('Invalid response from ML service');
        }

        const { summary, topics } = mlResponse.data;

        // Return success response
        res.json({
            summary: summary,
            topics: topics || [],
            status: 'success',
            processedAt: new Date().toISOString(),
            textLength: trimmedText.length
        });

        console.log('Summarization completed successfully');

    } catch (error) {
        console.error('Error in summarization endpoint:', error.message);

        // Handle different types of errors
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({
                error: 'ML service is not available. Please try again later.',
                status: 'error',
                code: 'SERVICE_UNAVAILABLE'
            });
        }

        if (error.code === 'ENOTFOUND') {
            return res.status(503).json({
                error: 'Cannot connect to ML service',
                status: 'error',
                code: 'CONNECTION_ERROR'
            });
        }

        if (error.response) {
            // ML service returned an error
            const statusCode = error.response.status || 500;
            const errorMessage = error.response.data?.error || 'ML service error';
            
            return res.status(statusCode).json({
                error: errorMessage,
                status: 'error',
                code: 'ML_SERVICE_ERROR'
            });
        }

        // General server error
        res.status(500).json({
            error: 'Internal server error occurred during text processing',
            status: 'error',
            code: 'INTERNAL_ERROR'
        });
    }
});

// Check ML service health
app.get('/api/ml-health', async (req, res) => {
    try {
        const response = await axios.get(`${FLASK_ML_URL}/health`, {
            timeout: 5000
        });
        
        res.json({
            mlService: response.data,
            status: 'connected'
        });
    } catch (error) {
        res.status(503).json({
            error: 'ML service is not available',
            status: 'disconnected',
            details: error.message
        });
    }
});

// Handle 404 errors - Fixed the catch-all route
app.use((req, res) => {
    res.status(404).json({
        error: 'Endpoint not found',
        status: 'error',
        path: req.path,
        method: req.method,
        availableEndpoints: [
            'GET /health',
            'POST /api/summarize',
            'GET /api/ml-health'
        ]
    });
});

// Global error handler
app.use((error, req, res, next) => {
    console.error('Unhandled error:', error);
    res.status(500).json({
        error: 'Internal server error',
        status: 'error'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 AutoNotes Backend Server running on port ${PORT}`);
    console.log(`📡 ML Service URL: ${FLASK_ML_URL}`);
    console.log(`🏥 Health check: http://localhost:${PORT}/health`);
    console.log(`📝 API endpoint: http://localhost:${PORT}/api/summarize`);
});
