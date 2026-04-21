// JavaScript principal para AgroTech

document.addEventListener('DOMContentLoaded', function() {
    // Fechar alertas automaticamente após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Formatação de campos de data
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Garante que o placeholder funcione corretamente
        if (!input.value) {
            input.placeholder = 'AAAA-MM-DD';
        }
    });
    
    // Confirmação para exclusões
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja realizar esta ação?')) {
                e.preventDefault();
            }
        });
    });
});

// Função para buscar dados meteorológicos
function fetchWeatherData(location) {
    fetch(`/api/weather/${encodeURIComponent(location)}`)
        .then(response => response.json())
        .then(data => {
            console.log('Dados meteorológicos:', data);
            // Aqui você pode atualizar a UI com os dados
        })
        .catch(error => {
            console.error('Erro ao buscar dados meteorológicos:', error);
        });
}

// Função para formatar valores monetários
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para formatar números decimais
function formatNumber(value, decimals = 2) {
    return new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(value);
}
