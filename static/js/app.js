// Client-side form validation
document.addEventListener('DOMContentLoaded', function() {
    // Add machine form validation
    const addMachineForm = document.querySelector('form[method="POST"]');
    if (addMachineForm) {
        addMachineForm.addEventListener('submit', function(e) {
            const ipInput = document.getElementById('ip_address');
            if (ipInput && !isValidIP(ipInput.value)) {
                e.preventDefault();
                alert('Please enter a valid IP address');
                ipInput.focus();
                return false;
            }
            return true;
        });
    }

    // Simple IP validation
    function isValidIP(ip) {
        return /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip);
    }

    // Flash message auto-hide
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });

    // Date input defaults
    const lastMaintenanceInput = document.getElementById('last_maintenance');
    if (lastMaintenanceInput && !lastMaintenanceInput.value) {
        const today = new Date().toISOString().split('T')[0];
        lastMaintenanceInput.value = today;
    }
});