/**
 * MasterInfo - Checkout Page
 * Step 1: Plano + Viabilidade (IXC real)
 * Step 2: Produtos Extras (add-ons)
 * Step 3: Cadastro (dados pessoais + endereco)
 * Step 4: Revisao + Finalizacao → Bitrix24
 */
(function () {
  'use strict';

  // ─── Config (loaded from config.json, fallback hardcoded) ───
  var PLANS = {};
  var ADDONS = [];
  var CHECKOUT_MODE = 'simples';
  var WHATSAPP_NUMBER = '5547989212991';

  var API_BASE = 'api/';

  // ─── Aliases de ID de plano ───
  // Os links do site (index.html) usam IDs por velocidade/linha (600, ultra-800...),
  // mas o config.json usa IDs nominais (lite-casa, ultra-familia...). Este mapa
  // traduz os IDs legados/do site para o ID canonico do config.
  var PLAN_ALIASES = {
    '600': 'lite-casa',
    '800': 'lite-familia',
    '1000': 'lite-home-office',
    'ultra-800': 'ultra-familia',
    'ultra-1000': 'ultra-home-office'
  };

  // ─── Tema do checkout (claro | black) ───
  function applyCheckoutTheme(tema) {
    var dark = tema === 'black';
    document.documentElement.setAttribute('data-theme', tema);
    var set = function (id, off) { var el = document.getElementById(id); if (el) el.disabled = off; };
    set('cssDark', !dark);  set('cssModalDark', !dark);
    set('cssLight', dark);  set('cssModalLight', dark);
  }

  // ─── Load config from JSON ───
  function loadCheckoutConfig(callback) {
    fetch('config.json?v=' + Date.now())
      .then(function(r) { return r.json(); })
      .then(function(cfg) {
        // Checkout mode
        CHECKOUT_MODE = cfg.checkout && cfg.checkout.modo || 'simples';
        WHATSAPP_NUMBER = cfg.checkout && cfg.checkout.whatsapp || '5547989212991';

        // Tema (claro | black) — definido no admin, global
        var tema = (cfg.checkout && cfg.checkout.tema) || 'claro';
        try { localStorage.setItem('mi_checkout_tema', tema); } catch (e) {}
        applyCheckoutTheme(tema);

        // Plans: convert array to object
        PLANS = {};
        (cfg.planos || []).forEach(function(p) {
          PLANS[p.id] = {
            id: p.id,
            name: p.nome,
            speed: p.velocidade,
            speedUnit: p.unidade,
            // Preco CHEIO (sem desconto). Fallbacks defensivos p/ nunca ficar undefined.
            price: (p.precoCheio != null ? p.precoCheio : (p.precoPontual != null ? p.precoPontual : p.preco)) || 0,
            // Preco PONTUAL (com desconto pagando em dia). Fallback = cheio.
            pricePontual: (p.precoPontual != null ? p.precoPontual : (p.precoCheio != null ? p.precoCheio : p.preco)) || 0,
            features: p.features || [],
            includesTV: p.incluiTV || false,
            badge: p.badge || null,
          };
        });

        // Addons: convert from config format
        ADDONS = (cfg.addons || []).map(function(a) {
          return {
            id: a.id,
            name: a.nome,
            desc: a.descricao,
            icon: a.icone,
            price: a.preco,
            setup: a.instalacao || 0,
            unit: a.unidade || '/mes',
            includedWith: a.incluidoEm || [],
          };
        });

        callback();
      })
      .catch(function() {
        // Fallback: use defaults if config.json fails
        console.warn('[Checkout] config.json nao encontrado, usando valores padrao');
        PLANS = {
          'lite-400': { id: 'lite-400', name: 'Lite', speed: '400', speedUnit: 'Mega', price: 109, features: ['Wi-Fi incluso', 'Roteador em comodato', 'Instalacao gratis', 'Suporte local 7 dias'], includesTV: false, badge: null },
          'ultra-600': { id: 'ultra-600', name: 'Ultra+', speed: '600', speedUnit: 'Mega', price: 149, features: ['Ideal p/ smart home', 'Ate 10 dispositivos'], includesTV: true, badge: 'Mais vendido' },
          'giga-1000': { id: 'giga-1000', name: 'Giga', speed: '1', speedUnit: 'Giga', price: 179, features: ['Velocidade maxima', 'Gamers & streamers'], includesTV: true, badge: null },
        };
        ADDONS = [];
        callback();
      });
  }

  // ─── State ───
  var state = {
    currentStep: 1,
    plan: null,
    viabilidade: { cep: '', endereco: null, cto: null, viavel: false },
    addons: [],       // IDs of selected addons
    cliente: {
      nome: '', cpf: '', nascimento: '', rg: '',
      whatsapp: '', email: '',
      numero: '', complemento: '', referencia: '',
    },
    totalMensal: 0,
    totalInstalacao: 0,
  };

  // ─── Init ───
  function init() {
    var params = new URLSearchParams(window.location.search);
    var planoParam = params.get('plano');

    // Traduz ID legado/do site (ex: ultra-800) para o ID canonico do config
    if (planoParam && PLAN_ALIASES[planoParam]) {
      planoParam = PLAN_ALIASES[planoParam];
    }

    if (planoParam && PLANS[planoParam]) {
      selectPlan(planoParam);
    } else {
      renderPlanSelector();
    }

    if (CHECKOUT_MODE === 'simples') {
      initSimpleMode();
    } else {
      renderAddons();
    }

    updateSummary();
  }

  // ─── Simple Mode Setup ───
  function initSimpleMode() {
    // Update step bar: show only 2 steps
    var stepsBar = document.querySelector('.checkout-steps-bar');
    if (stepsBar) {
      stepsBar.innerHTML =
        '<div class="ck-step active" data-step="1">' +
          '<span class="ck-step-num">1</span>' +
          '<span class="ck-step-label">Plano</span>' +
        '</div>' +
        '<div class="ck-step-line"></div>' +
        '<div class="ck-step" data-step="2">' +
          '<span class="ck-step-num">2</span>' +
          '<span class="ck-step-label">Contato</span>' +
        '</div>';
    }

    // Replace step 2 content with simple contact form
    var step2 = document.getElementById('ckStep2');
    if (step2) {
      step2.innerHTML =
        '<h2 class="ck-title">Quase pronto!</h2>' +
        '<p class="ck-subtitle">Deixe seu contato e nosso time finaliza tudo pelo WhatsApp.</p>' +
        '<div class="ck-form-section">' +
          '<div class="ck-form-grid">' +
            '<div class="mi-field ck-field-full">' +
              '<label for="ck_simple_nome">Nome *</label>' +
              '<input type="text" id="ck_simple_nome" placeholder="Seu nome" autocomplete="name">' +
            '</div>' +
            '<div class="mi-field ck-field-full">' +
              '<label for="ck_simple_whatsapp">WhatsApp *</label>' +
              '<input type="tel" id="ck_simple_whatsapp" placeholder="(47) 99999-9999" maxlength="15" autocomplete="tel">' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="mi-error" id="ckSimpleError" style="display:none;"></div>' +
        '<div class="ck-step-nav">' +
          '<button type="button" class="ck-btn-back" onclick="goToStep(1)">' +
            '<i class="ph ph-arrow-left"></i> Voltar' +
          '</button>' +
          '<button type="button" class="ck-btn-submit" id="ckSimpleSubmit" onclick="submitSimple()">' +
            '<i class="ph-fill ph-whatsapp-logo"></i> Enviar pelo WhatsApp' +
          '</button>' +
        '</div>';
    }

    // Hide viabilidade section (not required in simple mode)
    var viabilidade = document.getElementById('ckViabilidade');
    if (viabilidade) viabilidade.style.display = 'none';

    // Update subtitle
    var subtitle = document.querySelector('#ckStep1 .ck-subtitle');
    if (subtitle) subtitle.textContent = 'Selecione o plano ideal para voce.';

    // Enable next button if plan already selected
    if (state.plan) {
      var nextBtn = document.getElementById('ckStep1Next');
      if (nextBtn) nextBtn.disabled = false;
    }

    // Hide steps 3 and 4
    var step3 = document.getElementById('ckStep3');
    var step4 = document.getElementById('ckStep4');
    if (step3) step3.remove();
    if (step4) step4.remove();

    // Apply phone mask to simple whatsapp field
    document.addEventListener('input', function (e) {
      if (e.target && e.target.id === 'ck_simple_whatsapp') {
        var v = e.target.value.replace(/\D/g, '');
        if (v.length > 11) v = v.slice(0, 11);
        if (v.length > 7) {
          e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
        } else if (v.length > 2) {
          e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2);
        } else if (v.length > 0) {
          e.target.value = '(' + v;
        }
      }
    });
  }

  // ─── Simple Mode Submit ───
  window.submitSimple = function () {
    var nome = (document.getElementById('ck_simple_nome') || {}).value || '';
    var whatsapp = (document.getElementById('ck_simple_whatsapp') || {}).value || '';
    var phoneDigits = whatsapp.replace(/\D/g, '');

    nome = nome.trim();

    if (!nome) {
      showCkError('ckSimpleError', 'Informe seu nome.');
      return;
    }
    if (phoneDigits.length < 10 || phoneDigits.length > 11) {
      showCkError('ckSimpleError', 'Informe um WhatsApp valido.');
      return;
    }

    hideCkError('ckSimpleError');

    var p = state.plan;
    var end = state.viabilidade.endereco;

    var msg = 'Ola! Gostaria de contratar a internet MasterInfo.\n\n';
    msg += '*Plano:* ' + p.name + ' ' + p.speed + ' ' + p.speedUnit + ' — R$ ' + formatPrice(p.price) + '/mes\n';
    msg += '*Nome:* ' + nome + '\n';
    if (end) {
      msg += '*Endereco:* ' + (end.logradouro || '') + ', ' + (end.bairro || '') + ' — ' + (end.cidade || '') + '/' + (end.uf || '') + '\n';
      msg += '*CEP:* ' + state.viabilidade.cep + '\n';
    }
    msg += '\nPode me ajudar a finalizar?';

    var whatsLink = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(msg);
    window.open(whatsLink, '_blank');

    // Show success inline
    var step2 = document.getElementById('ckStep2');
    if (step2) {
      step2.innerHTML =
        '<div class="ck-success">' +
          '<div class="ck-success-icon">' +
            '<svg width="80" height="80" viewBox="0 0 64 64">' +
              '<circle cx="32" cy="32" r="30" stroke-width="2" fill="rgba(34,197,94,0.1)"/>' +
              '<path d="M20 33l8 8 16-16" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' +
            '</svg>' +
          '</div>' +
          '<h2>Mensagem enviada!</h2>' +
          '<p class="ck-success-desc">Continue a conversa no WhatsApp para finalizar sua contratacao. Nosso time vai te ajudar com tudo!</p>' +
          '<a href="' + whatsLink + '" class="ck-btn-whatsapp" target="_blank">' +
            '<i class="ph-fill ph-whatsapp-logo"></i> Abrir WhatsApp novamente' +
          '</a>' +
          '<a href="index.html" class="ck-btn-back-home">' +
            '<i class="ph ph-arrow-left"></i> Voltar ao site' +
          '</a>' +
        '</div>';
    }

    // Update step bar
    document.querySelectorAll('.ck-step').forEach(function (el) {
      el.classList.add('completed');
      el.classList.remove('active');
    });
    document.querySelectorAll('.ck-step-line').forEach(function (el) {
      el.classList.add('active');
    });

    // Hide summaries
    var sidebar = document.getElementById('ckSidebar');
    if (sidebar) sidebar.style.display = 'none';
    var mobileSummary = document.getElementById('ckMobileSummary');
    if (mobileSummary) mobileSummary.style.display = 'none';
  };

  // ─── Plan Selection ───
  function selectPlan(planId) {
    state.plan = PLANS[planId];
    var container = document.getElementById('ckSelectedPlan');
    var selector = document.getElementById('ckPlanSelector');

    if (selector) selector.style.display = 'none';

    if (container) {
      var p = state.plan;
      container.innerHTML =
        '<div class="ck-plan-card selected">' +
          (p.badge ? '<span class="ck-plan-badge">' + p.badge + '</span>' : '') +
          '<div class="ck-plan-info">' +
            '<div class="ck-plan-name">' + p.name + '</div>' +
            '<div class="ck-plan-speed">' + p.speed + ' <small>' + p.speedUnit + '</small></div>' +
            '<div class="ck-plan-price">R$ ' + formatPrice(p.price) + ' <small>/mes</small></div>' +
            ((p.price - p.pricePontual) > 0 ? '<div class="ck-plan-desconto"><i class="ph-fill ph-check-circle"></i> R$ ' + formatPrice(p.pricePontual) + ' pagando em dia <strong>(R$ ' + formatPrice(p.price - p.pricePontual) + ' OFF)</strong></div>' : '') +
            '<ul class="ck-plan-features">' +
              p.features.map(function (f) { return '<li><i class="ph-fill ph-check-circle"></i> ' + f + '</li>'; }).join('') +
            '</ul>' +
          '</div>' +
          '<span class="ck-plan-change" onclick="changePlan()">Trocar plano</span>' +
        '</div>';
    }

    // In simple mode, enable next button as soon as plan is selected (no viabilidade needed)
    if (CHECKOUT_MODE === 'simples') {
      var nextBtn = document.getElementById('ckStep1Next');
      if (nextBtn) nextBtn.disabled = false;
    }

    updateSummary();
    if (CHECKOUT_MODE === 'completo') renderAddons();

    // Rastrear inicio do checkout
    if (typeof window.miTrack === 'function' && state.plan) {
      window.miTrack('begin_checkout', {
        plan: state.plan.name + ' ' + state.plan.speed + ' ' + state.plan.speedUnit,
        value: state.plan.price,
        currency: 'BRL'
      });
    }
  }

  window.changePlan = function () {
    state.plan = null;
    var container = document.getElementById('ckSelectedPlan');
    if (container) container.innerHTML = '';
    renderPlanSelector();
    updateSummary();
  };

  function renderPlanSelector() {
    var grid = document.getElementById('ckPlansGrid');
    var selector = document.getElementById('ckPlanSelector');
    if (!grid || !selector) return;

    selector.style.display = '';
    var html = '';
    var ids = Object.keys(PLANS);

    ids.forEach(function (id) {
      var p = PLANS[id];
      var isSelected = state.plan && state.plan.id === id;
      html +=
        '<div class="ck-plan-card' + (isSelected ? ' selected' : '') + '" onclick="pickPlan(\'' + id + '\')">' +
          (p.badge ? '<span class="ck-plan-badge">' + p.badge + '</span>' : '') +
          '<div class="ck-plan-name">' + p.name + '</div>' +
          '<div class="ck-plan-speed">' + p.speed + ' <small>' + p.speedUnit + '</small></div>' +
          '<div class="ck-plan-price">R$ ' + formatPrice(p.price) + ' <small>/mes</small></div>' +
        '</div>';
    });

    grid.innerHTML = html;
  }

  window.pickPlan = function (planId) {
    selectPlan(planId);
    var selector = document.getElementById('ckPlanSelector');
    if (selector) selector.style.display = 'none';
  };

  // ─── Step Navigation ───
  window.goToStep = function (step) {
    // Validate before moving forward
    if (typeof step === 'number' && step > state.currentStep) {
      if (state.currentStep === 1 && !state.plan) {
        showCkError('ckCepError', 'Selecione um plano antes de continuar.');
        return;
      }
      if (CHECKOUT_MODE === 'completo' && state.currentStep === 1 && !state.viabilidade.viavel) return;
    }

    state.currentStep = step;

    // Hide all step contents
    document.querySelectorAll('.ck-step-content').forEach(function (el) { el.style.display = 'none'; });

    // Show target
    var target;
    if (step === 'success') {
      target = document.getElementById('ckSuccess');
    } else {
      target = document.getElementById('ckStep' + step);
    }
    if (target) target.style.display = '';

    // Update step bar
    document.querySelectorAll('.ck-step').forEach(function (el) {
      var s = parseInt(el.getAttribute('data-step'));
      el.classList.remove('active', 'completed');
      if (typeof step === 'number') {
        if (s < step) el.classList.add('completed');
        else if (s === step) el.classList.add('active');
      } else {
        el.classList.add('completed');
      }
    });

    // Update step lines
    document.querySelectorAll('.ck-step-line').forEach(function (el, i) {
      var lineStep = i + 1;
      el.classList.toggle('active', typeof step === 'number' && lineStep < step);
    });

    // Step-specific logic
    if (step === 3) {
      prefillAddress();
      setTimeout(function () {
        var nome = document.getElementById('ck_nome');
        if (nome) nome.focus();
      }, 300);
    }

    if (step === 4) {
      renderReview();
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // ─── Viabilidade (CEP) ───
  window.verificarCobertura = function () {
    var cepInput = document.getElementById('ck_cep');
    var cep = (cepInput ? cepInput.value : '').replace(/\D/g, '');

    if (cep.length !== 8) {
      showCkError('ckCepError', 'Informe um CEP valido com 8 digitos.');
      return;
    }

    hideCkError('ckCepError');
    setCepLoading(true);

    // Hide previous results
    var addrResult = document.getElementById('ckAddressResult');
    var noCov = document.getElementById('ckNoCoverage');
    if (addrResult) addrResult.classList.add('mi-hidden');
    if (noCov) noCov.classList.add('mi-hidden');

    fetch(API_BASE + 'viabilidade.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cep: cep }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        setCepLoading(false);

        if (data.viavel) {
          state.viabilidade = {
            cep: cep,
            endereco: data.endereco,
            cto: data.cto,
            viavel: true,
          };

          // Show address
          var addrText = document.getElementById('ckAddressText');
          if (addrText && data.endereco) {
            addrText.textContent = (data.endereco.logradouro || '') + ', ' +
              (data.endereco.bairro || '') + ' - ' +
              (data.endereco.cidade || '') + '/' + (data.endereco.uf || '');
          }

          var ctoText = document.getElementById('ckCtoText');
          if (ctoText && data.cto) {
            ctoText.textContent = data.cto.nome + ' — ' + data.cto.portas_disponiveis + ' portas disponiveis (' + data.cto.distancia_metros + 'm)';
          }

          if (addrResult) addrResult.classList.remove('mi-hidden');

          // Enable next button
          var nextBtn = document.getElementById('ckStep1Next');
          if (nextBtn) nextBtn.disabled = false;
        } else {
          state.viabilidade.viavel = false;

          if (data.sem_cobertura || data.sem_porta) {
            var msg = document.getElementById('ckNoCoverageMsg');
            if (msg) msg.textContent = data.mensagem;
            state.viabilidade.endereco = data.endereco;
            if (noCov) noCov.classList.remove('mi-hidden');
          } else {
            showCkError('ckCepError', data.mensagem || 'Erro ao verificar cobertura.');
          }
        }
      })
      .catch(function () {
        setCepLoading(false);
        showCkError('ckCepError', 'Erro de conexao. Tente novamente.');
      });
  };

  // ─── CEP Mask ───
  document.addEventListener('input', function (e) {
    if (e.target && e.target.id === 'ck_cep') {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 8) v = v.slice(0, 8);
      if (v.length > 5) {
        e.target.value = v.slice(0, 5) + '-' + v.slice(5);
      } else {
        e.target.value = v;
      }
    }
  });

  // Enter key on CEP
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target && e.target.id === 'ck_cep') {
      e.preventDefault();
      verificarCobertura();
    }
  });

  // ─── Phone Mask ───
  document.addEventListener('input', function (e) {
    if (e.target && (e.target.id === 'ck_whatsapp' || e.target.id === 'ck_wait_phone')) {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 7) {
        e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
      } else if (v.length > 2) {
        e.target.value = '(' + v.slice(0, 2) + ') ' + v.slice(2);
      } else if (v.length > 0) {
        e.target.value = '(' + v;
      }
    }
  });

  // ─── CPF Mask ───
  document.addEventListener('input', function (e) {
    if (e.target && e.target.id === 'ck_cpf') {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 9) {
        e.target.value = v.slice(0, 3) + '.' + v.slice(3, 6) + '.' + v.slice(6, 9) + '-' + v.slice(9);
      } else if (v.length > 6) {
        e.target.value = v.slice(0, 3) + '.' + v.slice(3, 6) + '.' + v.slice(6);
      } else if (v.length > 3) {
        e.target.value = v.slice(0, 3) + '.' + v.slice(3);
      } else {
        e.target.value = v;
      }
    }
  });

  // ─── Date Mask (DD/MM/AAAA) ───
  document.addEventListener('input', function (e) {
    if (e.target && e.target.id === 'ck_nascimento') {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 8) v = v.slice(0, 8);
      if (v.length > 4) {
        e.target.value = v.slice(0, 2) + '/' + v.slice(2, 4) + '/' + v.slice(4);
      } else if (v.length > 2) {
        e.target.value = v.slice(0, 2) + '/' + v.slice(2);
      } else {
        e.target.value = v;
      }
    }
  });

  // ─── Add-ons ───
  function renderAddons() {
    var container = document.getElementById('ckAddonsList');
    if (!container) return;

    var html = '';
    ADDONS.forEach(function (addon) {
      var isIncluded = state.plan && addon.includedWith.indexOf(state.plan.id) !== -1;
      var isActive = state.addons.indexOf(addon.id) !== -1;

      var cls = 'ck-addon-card';
      if (isIncluded) cls += ' included';
      else if (isActive) cls += ' active';

      html +=
        '<div class="' + cls + '" onclick="toggleAddon(\'' + addon.id + '\')" data-addon="' + addon.id + '">' +
          '<div class="ck-addon-header">' +
            '<div class="ck-addon-icon"><i class="' + addon.icon + '"></i></div>' +
            '<div class="ck-addon-toggle"></div>' +
          '</div>' +
          '<div class="ck-addon-name">' + addon.name + '</div>' +
          '<div class="ck-addon-desc">' + addon.desc + '</div>' +
          (isIncluded
            ? '<div class="ck-addon-included-tag"><i class="ph-fill ph-check-circle"></i> Ja incluso no plano</div>'
            : '<div class="ck-addon-price">R$ ' + formatPrice(addon.price) + ' <small>' + addon.unit + '</small></div>' +
              (addon.setup > 0 ? '<div class="ck-addon-setup">+ R$ ' + formatPrice(addon.setup) + ' instalacao</div>' : '')
          ) +
        '</div>';
    });

    container.innerHTML = html;
  }

  window.toggleAddon = function (addonId) {
    // Find the addon
    var addon = ADDONS.find(function (a) { return a.id === addonId; });
    if (!addon) return;

    // Don't toggle if included in plan
    if (state.plan && addon.includedWith.indexOf(state.plan.id) !== -1) return;

    var idx = state.addons.indexOf(addonId);
    if (idx === -1) {
      state.addons.push(addonId);
    } else {
      state.addons.splice(idx, 1);
    }

    renderAddons();
    updateSummary();
  };

  // ─── Prefill Address from Viabilidade ───
  function prefillAddress() {
    var end = state.viabilidade.endereco;
    if (!end) return;

    var logField = document.getElementById('ck_logradouro');
    var bairroField = document.getElementById('ck_bairro');
    var cidadeField = document.getElementById('ck_cidade_uf');

    if (logField) logField.value = end.logradouro || '';
    if (bairroField) bairroField.value = end.bairro || '';
    if (cidadeField) cidadeField.value = (end.cidade || '') + '/' + (end.uf || '');
  }

  // ─── Validacao Step 3 ───
  window.validarEAvancar = function () {
    var nome = val('ck_nome');
    var cpf = val('ck_cpf');
    var nasc = val('ck_nascimento');
    var whats = val('ck_whatsapp');
    var email = val('ck_email');
    var numero = val('ck_numero');

    // Required fields
    if (!nome || !cpf || !nasc || !whats || !email || !numero) {
      showCkError('ckCadastroError', 'Preencha todos os campos obrigatorios (*).');
      return;
    }

    // CPF validation
    var cpfDigits = cpf.replace(/\D/g, '');
    if (cpfDigits.length !== 11 || !validaCPF(cpfDigits)) {
      showCkError('ckCadastroError', 'Informe um CPF valido.');
      return;
    }

    // Date validation
    var nascDigits = nasc.replace(/\D/g, '');
    if (nascDigits.length !== 8 || !validaData(nasc)) {
      showCkError('ckCadastroError', 'Informe uma data de nascimento valida (DD/MM/AAAA).');
      return;
    }

    // Phone validation
    var phoneDigits = whats.replace(/\D/g, '');
    if (phoneDigits.length < 10 || phoneDigits.length > 11) {
      showCkError('ckCadastroError', 'Informe um numero de WhatsApp valido.');
      return;
    }

    // Email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showCkError('ckCadastroError', 'Informe um e-mail valido.');
      return;
    }

    hideCkError('ckCadastroError');

    // Save to state
    state.cliente = {
      nome: nome,
      cpf: cpfDigits,
      nascimento: nasc,
      rg: val('ck_rg'),
      whatsapp: phoneDigits,
      email: email,
      numero: numero,
      complemento: val('ck_complemento'),
      referencia: val('ck_referencia'),
    };

    goToStep(4);
  };

  // ─── CPF Mod 11 ───
  function validaCPF(cpf) {
    if (/^(\d)\1{10}$/.test(cpf)) return false;

    var soma = 0;
    for (var i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    var resto = 11 - (soma % 11);
    var d1 = resto >= 10 ? 0 : resto;
    if (parseInt(cpf.charAt(9)) !== d1) return false;

    soma = 0;
    for (var j = 0; j < 10; j++) soma += parseInt(cpf.charAt(j)) * (11 - j);
    resto = 11 - (soma % 11);
    var d2 = resto >= 10 ? 0 : resto;
    return parseInt(cpf.charAt(10)) === d2;
  }

  // ─── Date Validation ───
  function validaData(str) {
    var parts = str.split('/');
    if (parts.length !== 3) return false;
    var d = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10);
    var y = parseInt(parts[2], 10);
    if (y < 1920 || y > 2010 || m < 1 || m > 12 || d < 1 || d > 31) return false;
    var date = new Date(y, m - 1, d);
    return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
  }

  // ─── Render Review ───
  function renderReview() {
    var container = document.getElementById('ckReviewContent');
    if (!container) return;

    calculateTotals();

    var p = state.plan;
    var end = state.viabilidade.endereco;
    var c = state.cliente;

    var html = '';

    // Plan block
    html += '<div class="ck-review-block">' +
      '<h4><i class="ph-fill ph-lightning"></i> Plano</h4>' +
      '<div class="ck-review-row"><span>Plano</span><span>' + p.name + ' ' + p.speed + ' ' + p.speedUnit + '</span></div>' +
      '<div class="ck-review-row"><span>Mensal</span><span>R$ ' + formatPrice(p.price) + '</span></div>' +
    '</div>';

    // Addons block (if any selected or included)
    var activeAddons = getActiveAddons();
    if (activeAddons.length > 0) {
      html += '<div class="ck-review-block"><h4><i class="ph-fill ph-plus-circle"></i> Extras</h4>';
      activeAddons.forEach(function (a) {
        var isIncl = p && a.includedWith.indexOf(p.id) !== -1;
        html += '<div class="ck-review-row"><span>' + a.name + '</span><span>' +
          (isIncl ? 'Incluso' : 'R$ ' + formatPrice(a.price) + '/mes') + '</span></div>';
        if (!isIncl && a.setup > 0) {
          html += '<div class="ck-review-row"><span>' + a.name + ' (instalacao)</span><span>R$ ' + formatPrice(a.setup) + '</span></div>';
        }
      });
      html += '</div>';
    }

    // Total block
    html += '<div class="ck-review-block">' +
      '<h4><i class="ph-fill ph-currency-circle-dollar"></i> Valores</h4>' +
      '<div class="ck-review-row ck-review-total"><span>Total mensal</span><span>R$ ' + formatPrice(state.totalMensal) + '/mes</span></div>';
    if (state.totalInstalacao > 0) {
      html += '<div class="ck-review-row"><span>Instalacao (unica)</span><span>R$ ' + formatPrice(state.totalInstalacao) + '</span></div>';
    }
    html += '</div>';

    // Customer block
    html += '<div class="ck-review-block">' +
      '<h4><i class="ph-fill ph-user"></i> Dados pessoais</h4>' +
      '<div class="ck-review-row"><span>Nome</span><span>' + c.nome + '</span></div>' +
      '<div class="ck-review-row"><span>CPF</span><span>' + formatCPF(c.cpf) + '</span></div>' +
      '<div class="ck-review-row"><span>Nascimento</span><span>' + c.nascimento + '</span></div>' +
      (c.rg ? '<div class="ck-review-row"><span>RG</span><span>' + c.rg + '</span></div>' : '') +
      '<div class="ck-review-row"><span>WhatsApp</span><span>' + formatPhone(c.whatsapp) + '</span></div>' +
      '<div class="ck-review-row"><span>E-mail</span><span>' + c.email + '</span></div>' +
    '</div>';

    // Address block
    var endCompleto = (end ? end.logradouro : '') + ', ' + c.numero +
      (c.complemento ? ' - ' + c.complemento : '') +
      ' - ' + (end ? end.bairro : '') +
      ', ' + (end ? end.cidade + '/' + end.uf : '');

    html += '<div class="ck-review-block">' +
      '<h4><i class="ph-fill ph-house"></i> Endereco de instalacao</h4>' +
      '<div class="ck-review-row"><span>Endereco</span><span>' + endCompleto + '</span></div>' +
      (c.referencia ? '<div class="ck-review-row"><span>Referencia</span><span>' + c.referencia + '</span></div>' : '') +
    '</div>';

    container.innerHTML = html;
  }

  // ─── Submit Order ───
  window.submitOrder = function () {
    var terms = document.getElementById('ckTerms');
    if (!terms || !terms.checked) {
      showCkError('ckReviewError', 'Voce precisa aceitar os termos de contratacao.');
      return;
    }

    hideCkError('ckReviewError');
    setSubmitLoading(true);

    var p = state.plan;
    var c = state.cliente;
    var end = state.viabilidade.endereco;

    var orderData = {
      // Plan
      plano_id: p.id,
      plano_nome: p.name + ' ' + p.speed + ' ' + p.speedUnit,
      plano_valor: p.price,
      // Addons
      addons: getActiveAddons().filter(function (a) {
        return a.includedWith.indexOf(p.id) === -1;
      }).map(function (a) {
        return { id: a.id, nome: a.name, valor: a.price, instalacao: a.setup };
      }),
      // Totals
      total_mensal: state.totalMensal,
      total_instalacao: state.totalInstalacao,
      // Customer
      nome: c.nome,
      cpf: c.cpf,
      nascimento: c.nascimento,
      rg: c.rg,
      whatsapp: c.whatsapp,
      email: c.email,
      // Address
      cep: state.viabilidade.cep,
      logradouro: end ? end.logradouro : '',
      numero: c.numero,
      complemento: c.complemento,
      bairro: end ? end.bairro : '',
      cidade: end ? end.cidade : '',
      uf: end ? end.uf : '',
      referencia: c.referencia,
      // CTO
      cto_nome: state.viabilidade.cto ? state.viabilidade.cto.nome : '',
    };

    // Prototype: simulate success
    setTimeout(function () {
      setSubmitLoading(false);

      // Generate order number
      var orderNum = 'MI-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random() * 99999)).padStart(5, '0');
      var orderEl = document.getElementById('ckOrderNumber');
      if (orderEl) orderEl.textContent = orderNum;

      // WhatsApp link
      var msg = 'Ola! Acabei de finalizar minha contratacao no site.\n';
      msg += 'Pedido: ' + orderNum + '\n';
      msg += 'Plano: ' + p.name + ' ' + p.speed + ' ' + p.speedUnit + '\n';
      msg += 'Nome: ' + c.nome + '\n';
      if (end) msg += 'Endereco: ' + (end.bairro || '') + ', ' + (end.cidade || '') + '\n';
      msg += '\nQuero finalizar minha contratacao!';

      var whatsLink = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(msg);
      var linkEl = document.getElementById('ckWhatsappLink');
      if (linkEl) linkEl.href = whatsLink;

      // Fire tracking: GA4 + Google Ads + Facebook Pixel (via hub)
      if (typeof window.miTrack === 'function') {
        window.miTrack('purchase', {
          plan: p.name + ' ' + p.speed + ' ' + p.speedUnit,
          value: state.totalMensal,
          currency: 'BRL',
          orderId: orderNumber
        });
      }
      // Fallback direto Facebook Pixel
      else if (typeof fbq === 'function') {
        fbq('track', 'Purchase', {
          content_name: p.name + ' ' + p.speed + ' ' + p.speedUnit,
          content_category: 'Internet Fibra',
          value: state.totalMensal,
          currency: 'BRL',
        });
      }

      console.log('[MasterInfo Checkout]', orderData);

      goToStep('success');

      // Hide sidebar on success
      var sidebar = document.getElementById('ckSidebar');
      if (sidebar) sidebar.style.display = 'none';
      var mobileSummary = document.getElementById('ckMobileSummary');
      if (mobileSummary) mobileSummary.style.display = 'none';
    }, 1800);
  };

  // ─── Waitlist ───
  window.submitWaitlist = function (e) {
    e.preventDefault();

    var name = val('ck_wait_name');
    var phone = (val('ck_wait_phone') || '').replace(/\D/g, '');

    if (!name || phone.length < 10) {
      showCkError('ckCepError', 'Preencha nome e WhatsApp valido.');
      return false;
    }

    var noCov = document.getElementById('ckNoCoverage');
    if (noCov) {
      noCov.innerHTML =
        '<div class="ck-success" style="padding:20px 0;">' +
          '<div class="ck-success-icon"><svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" class="mi-check-circle" stroke-width="2" fill="rgba(34,197,94,0.1)"/><path d="M20 33l8 8 16-16" class="mi-check-path" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' +
          '<h2 style="font-size:1.2rem;">Cadastro realizado!</h2>' +
          '<p style="color:var(--gray-400);font-size:0.9rem;">Vamos te avisar pelo WhatsApp<br>quando a fibra chegar no seu endereco.</p>' +
        '</div>';
    }

    console.log('[MasterInfo Waitlist]', { name: name, phone: phone, cep: state.viabilidade.cep });
    return false;
  };

  // ─── Summary Update ───
  function updateSummary() {
    calculateTotals();

    var planEl = document.getElementById('ckSummaryPlan');
    var addonsEl = document.getElementById('ckSummaryAddons');
    var totalEl = document.getElementById('ckSummaryTotal');
    var setupEl = document.getElementById('ckSummarySetup');
    var setupTotalEl = document.getElementById('ckSetupTotal');
    var setupContainer = document.getElementById('ckSummarySetup');

    // Plan
    if (planEl) {
      if (state.plan) {
        planEl.innerHTML =
          '<div class="ck-summary-plan-item">' +
            '<div><div class="ck-summary-plan-name">' + state.plan.name + ' ' + state.plan.speed + ' ' + state.plan.speedUnit + '</div>' +
            '<div class="ck-summary-plan-speed">' + state.plan.speed + ' ' + state.plan.speedUnit + '</div></div>' +
            '<div class="ck-summary-plan-price">R$ ' + formatPrice(state.plan.price) + '</div>' +
          '</div>';
      } else {
        planEl.innerHTML = '<span class="ck-summary-empty">Selecione um plano</span>';
      }
    }

    // Addons
    if (addonsEl) {
      var activeAddons = getActiveAddons();
      var html = '';
      activeAddons.forEach(function (a) {
        var isIncl = state.plan && a.includedWith.indexOf(state.plan.id) !== -1;
        html += '<div class="ck-summary-addon-item"><span>' + a.name + '</span><span>' +
          (isIncl ? 'Incluso' : '+ R$ ' + formatPrice(a.price)) + '</span></div>';
      });
      addonsEl.innerHTML = html;
      addonsEl.style.display = html ? '' : 'none';
    }

    // Total
    if (totalEl) totalEl.textContent = 'R$ ' + formatPrice(state.totalMensal);

    // Desconto "pagando em dia"
    var descEl = document.getElementById('ckSummaryDesconto');
    var descTxtEl = document.getElementById('ckSummaryDescontoTxt');
    if (descEl && descTxtEl) {
      if (state.descontoPontual > 0) {
        descTxtEl.textContent = 'R$ ' + formatPrice(state.totalPontual) + ' pagando em dia (R$ ' + formatPrice(state.descontoPontual) + ' OFF)';
        descEl.style.display = '';
      } else {
        descEl.style.display = 'none';
      }
    }

    // Setup
    if (setupContainer) {
      if (state.totalInstalacao > 0) {
        setupContainer.style.display = '';
        if (setupTotalEl) setupTotalEl.textContent = 'R$ ' + formatPrice(state.totalInstalacao);
      } else {
        setupContainer.style.display = 'none';
      }
    }

    // Mobile summary
    var mobilePlan = document.getElementById('ckMobilePlanName');
    var mobileTotal = document.getElementById('ckMobileTotal');
    if (mobilePlan) mobilePlan.textContent = state.plan ? state.plan.name + ' ' + state.plan.speed + ' ' + state.plan.speedUnit : '--';
    if (mobileTotal) mobileTotal.innerHTML = 'R$ ' + formatPrice(state.totalMensal) + '<small>/mes</small>';
  }

  function calculateTotals() {
    var mensal = state.plan ? state.plan.price : 0;
    var instalacao = 0;

    state.addons.forEach(function (addonId) {
      var addon = ADDONS.find(function (a) { return a.id === addonId; });
      if (!addon) return;
      // Don't charge if included in plan
      if (state.plan && addon.includedWith.indexOf(state.plan.id) !== -1) return;
      mensal += addon.price;
      instalacao += addon.setup;
    });

    state.totalMensal = mensal;
    state.totalInstalacao = instalacao;

    // Desconto "pagando em dia" (so do plano; addons nao tem desconto)
    var descontoPlano = state.plan ? Math.max(0, state.plan.price - state.plan.pricePontual) : 0;
    state.descontoPontual = descontoPlano;
    state.totalPontual = Math.max(0, state.totalMensal - descontoPlano);
  }

  function getActiveAddons() {
    // Return addons that are either selected or included in plan
    return ADDONS.filter(function (a) {
      var isIncluded = state.plan && a.includedWith.indexOf(state.plan.id) !== -1;
      var isSelected = state.addons.indexOf(a.id) !== -1;
      return isIncluded || isSelected;
    });
  }

  // ─── Mobile Summary Toggle ───
  window.toggleMobileSummary = function () {
    // Scroll to sidebar area or just show an alert with summary
    var sidebar = document.getElementById('ckSidebar');
    if (sidebar) {
      // On mobile sidebar is hidden, create a quick overlay
      var existing = document.getElementById('ckMobileOverlay');
      if (existing) {
        existing.remove();
        return;
      }

      var overlay = document.createElement('div');
      overlay.id = 'ckMobileOverlay';
      overlay.style.cssText = 'position:fixed;inset:0;z-index:95;background:rgba(0,0,0,0.7);display:flex;align-items:flex-end;justify-content:center;padding:16px;';
      overlay.onclick = function (e) { if (e.target === overlay) overlay.remove(); };

      var card = document.createElement('div');
      card.style.cssText = 'background:var(--gray-900);border:1px solid var(--gray-800);border-radius:20px 20px 0 0;padding:24px;width:100%;max-width:500px;max-height:70vh;overflow-y:auto;';
      card.innerHTML = sidebar.querySelector('.ck-summary-card').innerHTML;

      overlay.appendChild(card);
      document.body.appendChild(overlay);
    }
  };

  // ─── Helpers ───
  function val(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  function formatPrice(num) {
    return num.toFixed(2).replace('.', ',');
  }

  function formatCPF(cpf) {
    return cpf.slice(0, 3) + '.' + cpf.slice(3, 6) + '.' + cpf.slice(6, 9) + '-' + cpf.slice(9);
  }

  function formatPhone(phone) {
    if (phone.length === 11) {
      return '(' + phone.slice(0, 2) + ') ' + phone.slice(2, 7) + '-' + phone.slice(7);
    }
    return '(' + phone.slice(0, 2) + ') ' + phone.slice(2, 6) + '-' + phone.slice(6);
  }

  function showCkError(id, msg) {
    var el = document.getElementById(id);
    if (el) { el.textContent = msg; el.style.display = ''; }
  }

  function hideCkError(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'none';
  }

  function setCepLoading(loading) {
    var btn = document.getElementById('ckCepBtn');
    var text = document.getElementById('ckCepBtnText');
    var spin = document.getElementById('ckCepBtnLoading');
    if (btn) btn.disabled = loading;
    if (text) text.style.display = loading ? 'none' : '';
    if (spin) spin.style.display = loading ? 'inline-flex' : 'none';
  }

  function setSubmitLoading(loading) {
    var btn = document.getElementById('ckSubmitBtn');
    var text = document.getElementById('ckSubmitText');
    var spin = document.getElementById('ckSubmitLoading');
    if (btn) btn.disabled = loading;
    if (text) text.style.display = loading ? 'none' : '';
    if (spin) spin.style.display = loading ? 'inline-flex' : 'none';
  }

  // ─── Boot ───
  function boot() {
    loadCheckoutConfig(function() {
      init();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();
