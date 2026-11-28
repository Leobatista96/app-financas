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
    
    // Gerenciar navegação ativa (navbar do design system + fallbacks antigos)
    function initializeSidebar() {
    // Marcar item ativo no menu - navbar e offcanvas (legado)
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('#navbar .nav-link, .modern-sidebar .nav-link, .offcanvas .nav-link');
    
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
                            'rgba(34, 197, 94, 0.8)',
                            'rgba(239, 95, 60, 0.8)'
                        ],
                        borderColor: [
                            'rgba(34, 197, 94, 1)',
                            'rgba(239, 95, 60, 1)'
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
                            'rgba(239, 95, 60, 0.8)',
                            'rgba(34, 197, 94, 0.8)',
                            'rgba(59, 130, 246, 0.8)',
                            'rgba(168, 85, 247, 0.8)',
                            'rgba(12, 11, 7, 0.8)'
                        ],
                        borderColor: [
                            'rgba(239, 95, 60, 1)',
                            'rgba(34, 197, 94, 1)',
                            'rgba(59, 130, 246, 1)',
                            'rgba(168, 85, 247, 1)',
                            'rgba(12, 11, 7, 1)'
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
                    borderColor: 'rgba(34, 197, 94, 1)',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    tension: 0.4,
                    fill: true
                });
            }

            // Adicionar despesa se solicitado
            if (mode === 'expense' || mode === 'both') {
                datasets.push({
                    label: 'Despesa',
                    data: montlyData.total_month_value_expense,
                    borderColor: 'rgba(239, 95, 60, 1)',
                    backgroundColor: 'rgba(239, 95, 60, 0.1)',
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
                                color: 'rgb(94, 94, 94)',
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

    // Loading overlay em submits de formulário
    const loadingOverlay = document.getElementById('loadingOverlay');
    document.querySelectorAll('form').forEach(form => {
        if (form.dataset.noLoading === 'true') {
            return;
        }

        form.addEventListener('submit', function() {
            if (loadingOverlay) {
                loadingOverlay.classList.remove('d-none');
            }
        });
    });

    window.addEventListener('load', function() {
        if (loadingOverlay) {
            loadingOverlay.classList.add('d-none');
        }
    });

    // Alternar exibição da senha (botões [data-password-toggle])
    document.querySelectorAll('[data-password-toggle]').forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = document.getElementById(this.getAttribute('data-password-toggle'));
            const toggleIcon = this.querySelector('iconify-icon');
            if (!passwordInput) return;

            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                if (toggleIcon) toggleIcon.setAttribute('icon', 'lucide:eye-off');
            } else {
                passwordInput.type = 'password';
                if (toggleIcon) toggleIcon.setAttribute('icon', 'lucide:eye');
            }
        });
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

// Extrai apenas as mensagens de erro de um form, sem o nome técnico do campo.
// Aceita dicionário {campo: [mensagens]}, string simples ou vazio.
const flattenFormErrors = (errors) =>
    typeof errors === 'string'
        ? [errors]
        : Object.values(errors || {}).flatMap((values) =>
            Array.isArray(values) ? values : [values],
        );

// ===== MODAL TRANSACTION ===== 
const transactionFormErrors = document.getElementById('transactionFormErrors');

const renderTransactionFormErrors = (errors) => {
    if (!transactionFormErrors) return;

    const messages = flattenFormErrors(errors);

    transactionFormErrors.innerHTML = messages.length
        ? `Não foi possível salvar a transação. ${messages.join('<br>')}`
        : '<strong>Não foi possível salvar a transação.</strong>';
    transactionFormErrors.classList.remove('d-none');
};

const clearTransactionFormErrors = () => {
    if (!transactionFormErrors) return;
    transactionFormErrors.innerHTML = '';
    transactionFormErrors.classList.add('d-none');
};

document.addEventListener('DOMContentLoaded', function () {
  // Abrir modal ao clicar no botão
  document.querySelectorAll('#newTransactionButton').forEach((button) => {
    button.addEventListener('click', function () {
      clearTransactionFormErrors();
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
        clearTransactionFormErrors();

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
              renderTransactionFormErrors(data.errors || data.error || {});
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

    const messages = flattenFormErrors(errors);

    categorieFormErrors.innerHTML = messages.length
        ? `Não foi possível salvar a categoria. ${messages.join('<br>')}`
        : '<strong>Não foi possível salvar a categoria.</strong>';
    categorieFormErrors.classList.remove('d-none');
};

const clearCategorieFormErrors = () => {
    if (!categorieFormErrors) return;
    categorieFormErrors.innerHTML = '';
    categorieFormErrors.classList.add('d-none');
};

// ===== MODAL ACCOUNTS =====
const accountsFormErrors = document.getElementById('accountsFormErrors');

const renderAccountsFormErrors = (errors) => {
    if (!accountsFormErrors) return;

    const messages = flattenFormErrors(errors);

    accountsFormErrors.innerHTML = messages.length
        ? `Não foi possível salvar a conta. ${messages.join('<br>')}`
        : '<strong>Não foi possível salvar a conta.</strong>';
    accountsFormErrors.classList.remove('d-none');
};

const clearAccountsFormErrors = () => {
    if (!accountsFormErrors) return;
    accountsFormErrors.innerHTML = '';
    accountsFormErrors.classList.add('d-none');
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
        clearAccountsFormErrors();
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
        }
      })
      .catch((error) => {
        console.error('Erro:', error);
        showNotification('Erro ao criar categoria', 'danger');
      });
  });

    document.getElementById('accountsForm').addEventListener('submit', function (event) {
        event.preventDefault();
          event.stopImmediatePropagation();

    const form = document.getElementById('accountsForm');
    const formData = new FormData(form);
    const jsonData = {};

    formData.forEach((value, key) => (jsonData[key] = value));
        clearAccountsFormErrors();

    fetch('/new_account/', {
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
          showNotification('Conta criada com sucesso!', 'success');
          window.location.reload();
        } else {
          renderAccountsFormErrors(data.errors || data.error || {});
        }
      })
      .catch((error) => {
        console.error('Erro:', error);
        showNotification('Erro ao criar conta', 'danger');
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
  const editFormErrors = document.getElementById('editFormErrors');

  const renderEditFormErrors = (errors) => {
      if (!editFormErrors) return;

      const messages = flattenFormErrors(errors);

      editFormErrors.innerHTML = messages.length
          ? `Não foi possível atualizar a transação. ${messages.join('<br>')}`
          : '<strong>Não foi possível atualizar a transação.</strong>';
      editFormErrors.classList.remove('d-none');
  };

  const clearEditFormErrors = () => {
      if (!editFormErrors) return;
      editFormErrors.innerHTML = '';
      editFormErrors.classList.add('d-none');
  };

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#edit-btn').forEach((button) => {
      button.addEventListener('click', function () {
        const transactionId = this.getAttribute('data-id');

        fetch(`/transactions/${transactionId}/update/`)
          .then((response) => response.json())
          .then((data) => {
            document.getElementById('transactionId').value = data.id;
            document.getElementById('description').value = data.description;
            // Os selects usam o ID como value — preenche pelo ID.
            document.getElementById('category_name').value = data.category_id;
            document.getElementById('account_name').value = data.account_id;
            document.getElementById('due_date').value = data.due_date;
            document.getElementById('value').value = data.value;

            clearEditFormErrors();
            new bootstrap.Modal(document.getElementById('ModalChange')).show();
          });
      });
    });

    if (document.getElementById('saveChanges')) {
      document.getElementById('saveChanges').addEventListener('click', function () {
        const transactionId = document.getElementById('transactionId').value;

        fetch(`/transactions/${transactionId}/update/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          },
          body: JSON.stringify({
            // Chaves no padrão do TransactionModelForm.
            description: document.getElementById('description').value,
            category: document.getElementById('category_name').value,
            account: document.getElementById('account_name').value,
            due_date: document.getElementById('due_date').value,
            value: document.getElementById('value').value,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              showNotification('Transação atualizada com sucesso!', 'success');
              location.reload();
            } else {
              renderEditFormErrors(data.errors || data.error || {});
            }
          })
          .catch((error) => {
            console.error('Erro:', error);
            showNotification('Erro ao atualizar transação', 'danger');
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
                if (!data.success) {
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