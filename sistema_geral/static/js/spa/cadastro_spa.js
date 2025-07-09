
let selectedService = null;
let selectedTime = null;

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    setMinDate();
    renderServices();
    renderTimeSlots();
    setupEventListeners();
}

function setMinDate() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const minDate = tomorrow.toISOString().split('T')[0];
    document.getElementById('date').min = minDate;
}

function renderServices() {
    const grid = document.getElementById('servicesGrid');
    grid.innerHTML = services.map(service => `
        <div class="service-card" onclick="selectService(${service.id})">
            <input type="radio" name="service" value="${service.id}" id="service-${service.id}">
            <i class="${service.icon}"></i>
            <div class="service-name">${service.name}</div>
            <div class="service-duration">${service.duration}</div>
            <div class="service-price">${service.price}</div>
        </div>
    `).join('');
}

function renderTimeSlots() {
    const container = document.getElementById('timeSlots');
    container.innerHTML = timeSlots.map(time => `
        <div class="time-slot" onclick="selectTime('${time}')">
            <input type="radio" name="time" value="${time}" id="time-${time}">
            ${time}
        </div>
    `).join('');
}

function selectService(serviceId) {
    // Remove previous selection
    document.querySelectorAll('.service-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked service
    const selectedCard = document.querySelector(`#service-${serviceId}`).parentNode;
    selectedCard.classList.add('selected');
    
    selectedService = services.find(s => s.id === serviceId);
    document.getElementById(`service-${serviceId}`).checked = true;
    
    updateSummary();
}

function selectTime(time) {
    // Remove previous selection
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('selected');
    });
    
    // Add selection to clicked time
    const selectedSlot = document.querySelector(`#time-${time}`).parentNode;
    selectedSlot.classList.add('selected');
    
    selectedTime = time;
    document.getElementById(`time-${time}`).checked = true;
    
    updateSummary();
}

function updateSummary() {
    const guestName = document.getElementById('guestName').value;
    const date = document.getElementById('date').value;
    const roomNumber = document.getElementById('roomNumber').value;
    
    if (selectedService && selectedTime && guestName && date && roomNumber) {
        const summarySection = document.getElementById('summarySection');
        const summaryContent = document.getElementById('summaryContent');
        
        const formattedDate = new Date(date).toLocaleDateString('pt-BR');
        
        summaryContent.innerHTML = `
            <div class="summary-item">
                <span><i class="fas fa-user"></i> Hóspede:</span>
                <span>${guestName}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-door-open"></i> Quarto:</span>
                <span>${roomNumber}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-spa"></i> Serviço:</span>
                <span>${selectedService.name}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-clock"></i> Duração:</span>
                <span>${selectedService.duration}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-calendar"></i> Data:</span>
                <span>${formattedDate}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-clock"></i> Horário:</span>
                <span>${selectedTime}</span>
            </div>
            <div class="summary-item">
                <span><i class="fas fa-money-bill"></i> <strong>Total:</strong></span>
                <span><strong>${selectedService.price}</strong></span>
            </div>
        `;
        
        summarySection.style.display = 'block';
    } else {
        document.getElementById('summarySection').style.display = 'none';
    }
}

function setupEventListeners() {
    // Update summary when form fields change
    document.getElementById('guestName').addEventListener('input', updateSummary);
    document.getElementById('date').addEventListener('change', updateSummary);
    document.getElementById('roomNumber').addEventListener('input', updateSummary);
    
    // Phone mask
    document.getElementById('phone').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        value = value.replace(/(\d{2})(\d)/, '($1) $2');
        value = value.replace(/(\d{5})(\d)/, '$1-$2');
        e.target.value = value;
    });
}

function resetForm() {
    if (confirm('Tem certeza que deseja limpar todos os dados do formulário?')) {
        document.getElementById('reservationForm').reset();
        
        // Clear selections
        document.querySelectorAll('.service-card, .time-slot').forEach(el => {
            el.classList.remove('selected');
        });
        
        selectedService = null;
        selectedTime = null;
        
        // Hide summary
        document.getElementById('summarySection').style.display = 'none';
        
        // Hide messages
        document.getElementById('successMessage').style.display = 'none';
        document.getElementById('errorMessage').style.display = 'none';
        
        setMinDate();
    }
}

function goBack() {
    if (confirm('Deseja sair sem salvar? Todos os dados serão perdidos.')) {
        // In a real application, this would navigate back
        alert('Voltando ao painel principal...');
    }
}

// Form submission
document.getElementById('reservationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validate required fields
    const requiredFields = ['guestName', 'phone', 'roomNumber', 'date'];
    let isValid = true;
    
    requiredFields.forEach(field => {
        const input = document.getElementById(field);
        if (!input.value.trim()) {
            input.style.borderColor = '#e53e3e';
            isValid = false;
        } else {
            input.style.borderColor = '#e2e8f0';
        }
    });
    
    if (!selectedService) {
        document.getElementById('errorText').textContent = 'Por favor, selecione um serviço.';
        document.getElementById('errorMessage').style.display = 'block';
        isValid = false;
    }
    
    if (!selectedTime) {
        document.getElementById('errorText').textContent = 'Por favor, selecione um horário.';
        document.getElementById('errorMessage').style.display = 'block';
        isValid = false;
    }
    
    if (!isValid) {
        return;
    }
    
    // Show loading state
    const submitBtn = document.getElementById('submitBtn');
    const originalContent = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Processando...';
    submitBtn.disabled = true;
    
    // Hide error message
    document.getElementById('errorMessage').style.display = 'none';
    
    // Simulate API call
    setTimeout(() => {
        // Show success message
        document.getElementById('successMessage').style.display = 'block';
        document.getElementById('summarySection').style.display = 'none';
        
        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ 
            behavior: 'smooth' 
        });
        
        // Reset button
        submitBtn.innerHTML = originalContent;
        submitBtn.disabled = false;
        
        // Auto-reset form after 3 seconds
        setTimeout(() => {
            resetForm();
        }, 3000);
        
    }, 2500);
});
