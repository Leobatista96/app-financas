// ===== JAVASCRIPT MODERNO PARA INTERATIVIDADE =====

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initializeAnimations();
    initializeSidebar();
    initializeTooltips();
    initializeCharts();
    initializeNotifications();
    getChartCategoryData();
    getMontlyChartData();
    getCategorieRevenueExpenseFilter();
    
    // Adicionar classes de animação aos elementos
    function initializeAnimations() {
        const cards = document.querySelectorAll('.modern-card, .metric-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('animate-fade-in-up');
        });
        
        const sidebarItems = document.querySelectorAll('.modern-sidebar .nav-link');
        sidebarItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
            item.classList.add('animate-fade-in-left');
        });
    }
    
    // Gerenciar sidebar responsiva
    function initializeSidebar() {
    // Marcar item ativo no menu - tanto desktop quanto mobile
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.modern-sidebar .nav-link, .offcanvas .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Remover classe active de todos os links primeiro
        link.classList.remove('active');
        
        // Adicionar active apenas se o caminho for exatamente igual
        // OU se for a home e o caminho atual for '/'
        if (href && href !== '#') {
            // Normalizar os caminhos removendo trailing slash
            const normalizedHref = href.replace(/\/$/, '');
            const normalizedPath = currentPath.replace(/\/$/, '');
            
            // Comparação exata do caminho
            if (normalizedHref === normalizedPath) {
                link.classList.add('active');
            }
            // Caso especial para home/dashboard
            else if (normalizedHref === '' && normalizedPath === '') {
                link.classList.add('active');
            }
        }
    });
    
    // Auto-close mobile menu when clicking on links
    const mobileNavLinks = document.querySelectorAll('.offcanvas .nav-link');
    const mobileOffcanvas = document.querySelector('#sidebarMenuLabel');
    
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                // Close the offcanvas
                const bsOffcanvas = bootstrap.Offcanvas.getInstance(mobileOffcanvas);
                if (bsOffcanvas) {
                    bsOffcanvas.hide();
                }
            }
        });
    });
}
    
    // Inicializar tooltips do Bootstrap
    function initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    function getMontlyChartData(){
        const montlyChartData = document.getElementById('montly-chart-data');
        if (montlyChartData) {
            try {
                const data = JSON.parse(montlyChartData.textContent);
                console.log('Dados do grafico de mes carregado', data)
                return data
            }
            catch (e) {
                console.error('Erro ao carregar grafico de mes', e);
                return null;
            }
        }
    }

    function getChartCategoryData() {
        const scriptElement = document.getElementById('chart-data');
        if (scriptElement) {
            try {
                const data = JSON.parse(scriptElement.textContent);
                console.log('Dados do gráfico de categoria carregado', data)
                return data;
            }
            catch (e) {
                console.error('Erro ao carregar grafico de categoria', e);
                return null;
            }
        }
    }

    function getCategorieRevenueExpenseFilter() {
        const revenueBtn = document.getElementById('categoriesRevenuesFilterButton');
        const expenseBtn = document.getElementById('categoriesExpensesFilterButton');
        const tableRows = document.querySelectorAll('.transaction-row[data-category-type]');

        function filterCategories(type) {
            tableRows.forEach(row => {
                const categoryType = row.getAttribute('data-category-type');
                if (type === 'all') {
                    row.style.display = '';
                } else if (categoryType === type) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }
        
        if (revenueBtn) {
            revenueBtn.addEventListener('click', function (e) {
                e.preventDefault();
                filterCategories('revenue');
            });
        }

        if (expenseBtn) {
            expenseBtn.addEventListener('click', function (e) {
                e.preventDefault();
                filterCategories('expense');
            });
        }
    }
    
    // Inicializar gráficos (Chart.js)
    function initializeCharts() {
        console.log('Iniciando gráficos');

        if (typeof Chart === 'undefined'){
            console.error('Chart.js não carregado');
            return;
        }
        const chartData = getChartCategoryData();
        const montlyData = getMontlyChartData();

        console.log('Chart data:', {chartData, montlyData});

        const revenueExpenseCtx = document.getElementById('revenueExpenseChart');

        if (revenueExpenseCtx && chartData.total_recipes) {

            new Chart(revenueExpenseCtx, {
                type: 'doughnut',
                data: {
                    labels: chartData.total_recipes.labels,
                    datasets: [{
                        data: chartData.total_recipes.data,
                        backgroundColor: [
                            'rgba(74, 222, 128, 0.8)',
                            'rgba(239, 68, 68, 0.8)'
                        ],
                        borderColor: [
                            'rgba(74, 222, 128, 1)',
                            'rgba(239, 68, 68, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                font: {
                                    size: 14,
                                    weight: '500'
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // Gráfico de gastos por categoria
        const categoryCtx = document.getElementById('categoryChart');
        if (categoryCtx && chartData.categories) {
            new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: chartData.categories.labels,
                    datasets: [{
                        label: ' Total',
                        data: chartData.categories.values,
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(240, 147, 251, 0.8)',
                            'rgba(74, 222, 128, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(239, 68, 68, 0.8)'
                        ],
                        borderColor: [
                            'rgba(102, 126, 234, 1)',
                            'rgba(240, 147, 251, 1)',
                            'rgba(74, 222, 128, 1)',
                            'rgba(251, 191, 36, 1)',
                            'rgba(239, 68, 68, 1)'
                        ],
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }

        // Gráfico de evolução mensal
        const monthlyCtx = document.getElementById('monthlyChart');

        function renderMonthlyChart(mode = 'both') {
            if (!monthlyCtx || !montlyData) {
                console.warn('monthlyCtx ou montlyData não disponível', { monthlyCtx, montlyData });
                return;
            }

            const datasets = [];

            // Adicionar receita se solicitado
            if (mode === 'revenue' || mode === 'both') {
                datasets.push({
                    label: 'Receita',
                    data: montlyData.total_month_value_revenue,
                    borderColor: 'rgba(74, 222, 128, 1)',
                    backgroundColor: 'rgba(74, 222, 128, 0.1)',
                    tension: 0.4,
                    fill: true
                });
            }

            // Adicionar despesa se solicitado
            if (mode === 'expense' || mode === 'both') {
                datasets.push({
                    label: 'Despesa',
                    data: montlyData.total_month_value_expense,
                    borderColor: 'rgba(239, 68, 68, 1)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    tension: 0.4,
                    fill: true
                });
            }

            if (window.monthlyChartInstance) {
                window.monthlyChartInstance.destroy();
            }

            window.monthlyChartInstance = new Chart(monthlyCtx, {
                type: 'line',
                data: {
                    labels: montlyData.month_labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 10,
                                color: 'rgb(255, 255, 255)',
                                font: {
                                    size: 15,
                                    weight: 'normal',
                                }
                            }
                        }
                    },
                    elements: {
                        point: {
                            radius: 5,
                            hoverRadius: 8,
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }

        // Renderizar com ambos inicialmente
        console.log('Tentando renderizar gráfico mensal com dados:', { montlyData, monthlyCtx });
        renderMonthlyChart('both');


        // Listeners dos botões
        const revenueBtn = document.getElementById('revenue-filter');
        if (revenueBtn) {
            revenueBtn.addEventListener('click', function (e) {
                e.preventDefault();
                renderMonthlyChart('revenue');
            });
        }

        const expenseBtn = document.getElementById('expense-filter');
        if (expenseBtn) {
            expenseBtn.addEventListener('click', function (e) {
                e.preventDefault();
                renderMonthlyChart('expense');
            });
        }

        const bothBtn = document.getElementById('both-filter');
        if (bothBtn) {
            bothBtn.addEventListener('click', function (e) {
                e.preventDefault();
                renderMonthlyChart('both');
            });
        }
    }
    
    // Sistema de notificações
    function initializeNotifications() {
        window.showNotification = function(message, type = 'info', duration = 5000) {
            const toast = document.createElement('div');
            toast.className = `toast toast-modern align-items-center text-white bg-${type} border-0`;
            toast.setAttribute('role', 'alert');
            toast.setAttribute('aria-live', 'assertive');
            toast.setAttribute('aria-atomic', 'true');
            
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            
            // Container para toasts
            let toastContainer = document.querySelector('.toast-container');
            if (!toastContainer) {
                toastContainer = document.createElement('div');
                toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
                toastContainer.style.zIndex = '1060';
                document.body.appendChild(toastContainer);
            }
            
            toastContainer.appendChild(toast);
            
            const bsToast = new bootstrap.Toast(toast, {
                autohide: true,
                delay: duration
            });
            
            bsToast.show();
            
            // Remover toast após ser ocultado
            toast.addEventListener('hidden.bs.toast', function() {
                toast.remove();
            });
        };
    }
    
    // Função para formatar valores monetários
    window.formatCurrency = function(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    };
    
    // Função para animar contadores
    window.animateCounter = function(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = progress * (end - start) + start;
            element.textContent = formatCurrency(current);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };
    
    // Inicializar contadores animados
    const counterElements = document.querySelectorAll('[data-counter]');
    counterElements.forEach(element => {
        const target = parseFloat(element.getAttribute('data-counter').trim());
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(element, 0, target, 2000);
                    observer.unobserve(element);
                }
            });
        });
        observer.observe(element);
    });
    
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Lazy loading para imagens
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('loading');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // Auto-hide alerts
    const alerts = document.querySelectorAll('.alert[data-auto-hide]');
    alerts.forEach(alert => {
        const delay = parseInt(alert.getAttribute('data-auto-hide')) || 5000;
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, delay);
    });
});

// ===== UTILITY FUNCTIONS =====

// Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Local storage helpers
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    
    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return defaultValue;
        }
    },
    
    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// ===== MODAL TRANSACTION ===== 
document.addEventListener('DOMContentLoaded', function () {
  // Abrir modal ao clicar no botão
  document.querySelectorAll('#newTransactionButton').forEach((button) => {
    button.addEventListener('click', function () {
      new bootstrap.Modal(document.getElementById('ModalTransaction')).show();
    });
  });

  // Interceptar submit do formulário
  const form = document.getElementById('transactionForm');
  if (form) {
    form.addEventListener(
      'submit',
      function (e) {
        e.preventDefault(); // Prevenir reload da página
        e.stopPropagation(); // Evitar que o evento dispare listeners globais

        const submitBtn = document.getElementById('saveTransaction');
        submitBtn.disabled = true;

        let formData = new FormData(form);
        let jsonData = {};

        formData.forEach((value, key) => (jsonData[key] = value));

        // Get the CSRF token and URL
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const actionUrl = form.getAttribute('data-action') || '/new_transaction/';

        fetch(actionUrl, {
          method: 'POST',
          body: JSON.stringify(jsonData),
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // Mostrar notificação
              showNotification('Transação Cadastrada com Sucesso!', 'success');

              // Fechar modal
              const modal = bootstrap.Modal.getInstance(
                document.getElementById('ModalTransaction'),
              );
              modal.hide();

              // Limpar formulário
              form.reset();

              // Recarregar página após breve delay para atualizar a tabela
              setTimeout(() => {
                window.location.reload();
              }, 1500);
            } else {
              showNotification(
                'Erro ao salvar transação: ' + JSON.stringify(data.errors),
                'danger',
              );
            }
          })
          .catch((error) => {
            console.error('Erro:', error);
            showNotification('Erro ao salvar transação', 'danger');
          })
          .finally(() => {
            submitBtn.disabled = false;
          });
      },
      true,
    ); // Captura na fase de captura para interceptar antes do listener global
  }
});

// ===== MODAL CATEGORIE =====
const categorieFormErrors = document.getElementById('categorieFormErrors');

const renderCategorieFormErrors = (errors) => {
    if (!categorieFormErrors) return;

    const messages = Object.entries(errors || {}).flatMap(([field, values]) =>
        (Array.isArray(values) ? values : [values]).map((value) =>
            field === '__all__' ? value : `${field}: ${value}`,
        ),
    );

    categorieFormErrors.innerHTML = messages.length
        ? `<strong>Não foi possível salvar a categoria. Categoria com este nome já existe.</strong><br>`
        : '<strong>Não foi possível salvar a categoria.</strong>';
    categorieFormErrors.classList.remove('d-none');
};

const clearCategorieFormErrors = () => {
    if (!categorieFormErrors) return;
    categorieFormErrors.innerHTML = '';
    categorieFormErrors.classList.add('d-none');
};

if (document.getElementById('categorieForm')) {
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.addcategoriebutton').forEach((button) => {
      button.addEventListener('click', function () {
                clearCategorieFormErrors();
        new bootstrap.Modal(document.getElementById('ModalCategorie')).show();
      });
    });
    });

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.addaccountbutton').forEach((button) => {
      button.addEventListener('click', function () {
        new bootstrap.Modal(document.getElementById('ModalAccounts')).show();
      });
    });
  });


    document.getElementById('categorieForm').addEventListener('submit', function (event) {
        event.preventDefault();
          event.stopImmediatePropagation();

    const form = document.getElementById('categorieForm');
    const formData = new FormData(form);
    const jsonData = {};

    formData.forEach((value, key) => (jsonData[key] = value));
        clearCategorieFormErrors();

    fetch('/new_categorie/', {
      method: 'POST',
      body: JSON.stringify(jsonData),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showNotification('Categoria criada com sucesso!', 'success');
          window.location.reload();
        } else {
                    renderCategorieFormErrors(data.errors || data.error || {});
          showNotification('Erro ao criar categoria', 'danger');
        }
      })
      .catch((error) => {
        console.error('Erro:', error);
        showNotification('Erro ao criar categoria', 'danger');
      });
  });
}

// ===== MODAL TRANSACTION DELETE  =====
let transactionIdToDelete = null;

if (document.querySelectorAll('.delete-btn').length > 0) {
  document.querySelectorAll('.delete-btn').forEach((button) => {
    button.addEventListener('click', function () {
      transactionIdToDelete = this.getAttribute('data-id');
      
    });
  });
}

if (document.getElementById('confirmDelete')) {
  document.getElementById('confirmDelete').addEventListener('click', function () {
    if (transactionIdToDelete) {
      fetch(`/transaction/${transactionIdToDelete}/delete/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            showNotification('Transação excluída com sucesso!', 'success');
            document.getElementById(`transaction-row-${transactionIdToDelete}`).remove();
          } else {
            showNotification('Erro ao excluir a transação.', 'danger');
          }
          transactionIdToDelete = null;
          const modal = bootstrap.Modal.getInstance(document.getElementById('ModalDelete'));
          if (modal) {
            modal.hide();
          }
          location.reload();
        });
    }
  });
}



// ===== MODAL TRANSACTION EDIT =====
if (document.getElementById('editForm')) {
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#edit-btn').forEach((button) => {
      button.addEventListener('click', function () {
        const transactionId = this.getAttribute('data-id');

        fetch(`/transactions/${transactionId}/update/`)
          .then((response) => response.json())
          .then((data) => {
            document.getElementById('transactionId').value = data.id;
            document.getElementById('description').value = data.description;
            document.getElementById('category_id').value = data.category_id;
            document.getElementById('category_name').value = data.category_name;
            document.getElementById('due_date').value = data.due_date;
            document.getElementById('account_id').value = data.account_id;
            document.getElementById('account_name').value = data.account_name;
            document.getElementById('value').value = data.value;
            document.getElementById('created_at').value = data.created_at;

            new bootstrap.Modal(document.getElementById('ModalChange')).show();
          });
      });
    });

    if (document.getElementById('saveChanges')) {
      document.getElementById('saveChanges').addEventListener('click', function () {
        const transactionId = document.getElementById('transactionId').value;
        const description = document.getElementById('description').value;
        const category_id = document.getElementById('category_id').value;
        const category_name = document.getElementById('category_name').value;
        const due_date = document.getElementById('due_date').value;
        const account_id = document.getElementById('account_id').value;
        const account_name = document.getElementById('account_name').value;
        const value = document.getElementById('value').value;

        fetch(`/transactions/${transactionId}/update/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
          body: JSON.stringify({
            description: description,
            category_id: category_id,
            account: account_id,
            due_date: due_date,
            value: value,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            showNotification('Transação atualizada com sucesso!', 'success');
            location.reload();
          });
      });
    }
  });
}

// === MODAL ACCOUNT DELETE ====

let accountIdToDelete = null;

if (document.querySelectorAll('.delete-account-btn').length > 0) {
  document.querySelectorAll('.delete-account-btn').forEach((button) => {
    button.addEventListener('click', function () {
      accountIdToDelete = this.getAttribute('data-id');
      
    });
  });
}

if (document.getElementById('confirmDelete')) {
    document.getElementById('confirmDelete').addEventListener('click', function(){
        if (accountIdToDelete) {
            fetch(`/account/${accountIdToDelete}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    showNotification('Conta excluída com sucesso!', 'success');
                } else {
                    showNotification('Erro ao excluir a conta', 'danger');
                }
                accountIdToDelete = null;
                const modal = bootstrap.Modal.getInstance(document.getElementById('ModalDelete'));
                if (modal) {
                    modal.hide();
                }
                location.reload();
            })
        }
    })
}

// ==== MODAL ACCOUNT EDIT ====

if (document.getElementById('editaccountForm')) {
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.edit-account-btn').forEach((button) =>{
            button.addEventListener('click', function () {
                const accountId = this.getAttribute('data-id');

                fetch(`/account/${accountId}/update`)
                    .then((response) => response.json())
                    .then((data) => {
                        document.getElementById('account_name').value = data.name;
                        document.getElementById('account_value').value = data.value;
                        document.getElementById('account_categorie_name').value = data.categorie;
                        
                        new bootstrap.Modal(document.getElementById('#ModalAccountChange')).show();
                });
            });
        });
    });
}


// ===== DASHBOARD =====
if (document.querySelectorAll('[data-quick-action]').length > 0) {
  document.addEventListener('DOMContentLoaded', function () {
    // Refresh data every 5 minutes
    setInterval(function () {
      console.log('Refreshing dashboard data...');
    }, 300000);

    // Quick action buttons
    document.querySelectorAll('[data-quick-action]').forEach((button) => {
      button.addEventListener('click', function () {
        const action = this.getAttribute('data-quick-action');
        handleQuickAction(action);
      });
    });
  });
}