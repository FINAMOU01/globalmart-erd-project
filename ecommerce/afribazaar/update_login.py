#!/usr/bin/env python
"""Update login.html template"""

login_html = """{% extends 'base.html' %}
{% load static %}

{% block title %}Welcome Back 👋{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-left-panel" style="background: linear-gradient(135deg, var(--color-black), var(--color-gold));">
        <div class="auth-left-content">
            <h2>Welcome Back 👋</h2>
            <p>Sign in to your AfriBazaar account</p>
        </div>
    </div>
    <div class="auth-right-panel">
        <div class="auth-form-card">
            <h2>Sign In</h2>
            <p class="form-subtitle">Welcome back to AfriBazaar</p>
            
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
            
            <form method="post">
                {% csrf_token %}
                <div class="form-group">
                    {{ form.username.label_tag }}
                    {{ form.username }}
                    {% if form.username.errors %}
                        <div class="error-message">
                            {{ form.username.errors|first }}
                        </div>
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.password.label_tag }}
                    {{ form.password }}
                    {% if form.password.errors %}
                        <div class="error-message">
                            {{ form.password.errors|first }}
                        </div>
                    {% endif %}
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>
            
            <div class="auth-footer">
                <p>New customer? <a href="{% url 'customer_register' %}" class="auth-link">Register here</a></p>
                <p>Are you an artisan? <a href="{% url 'artisan_register' %}" class="auth-link">Register here</a></p>
                <p><a href="#" class="auth-link forgot-password">Forgot password?</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

with open('templates/accounts/login.html', 'w') as f:
    f.write(login_html)

print("✓ Updated login.html")
