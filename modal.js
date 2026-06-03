/**
 * MasterInfo - Modal Multi-Step de Contratação
 * Step 1: Verificar cobertura (CEP → API viabilidade)
 * Step 2: Dados pessoais (nome, whatsapp, email)
 * Step 3: Sucesso → redireciona WhatsApp (Rafa)
 */
(function () {
  'use strict';

  var IS_WP = typeof fazupCRM !== 'undefined';
  var API_BASE = IS_WP ? fazupCRM.ajaxurl : 'api/';

  // Estado do modal
  var state = {
    step: 1,
    plan: '',
    endereco: null,
    cto: null,
  };

  // ─── Abrir Modal ───
  window.openLeadModal = function (planName) {
    var modal = document.getElementById('miModal');
    if (!modal) return;

    // Reset state
    state = { step: 1, plan: planName || '', endereco: null, cto: null };

    // Reset forms
    var forms = modal.querySelectorAll('form');
    forms.forEach(function (f) { f.reset(); });

    // Plan tag
    var planTag = document.getElementById('miPlanTag');
    var planInput = document.getElementById('mi_plan');
    if (planName) {
      if (planTag) {
        planTag.innerHTML = '<i class="ph-fill ph-lightning"></i> ' + planName;
        planTag.classList.remove('mi-hidden');
      }
      if (planInput) planInput.value = planName;
    } else {
      if (planTag) planTag.classList.add('mi-hidden');
      if (planInput) planInput.value = '';
    }

    // Rastrear abertura do modal (jornada + funil)
    if (typeof window.miTrack === 'function') window.miTrack('modal_open', { plan: planName || '' });

    // Show step 1, hide all others
    goToStep(1);

    // Hide all errors
    modal.querySelectorAll('.mi-error').forEach(function (el) { el.style.display = 'none'; });

    // Show modal
    modal.style.display = 'flex';
    modal.offsetHeight;
    modal.classList.add('mi-visible');
    document.body.style.overflow = 'hidden';

    // Focus CEP
    setTimeout(function () {
      var cepInput = document.getElementById('mi_cep');
      if (cepInput) cepInput.focus();
    }, 300);
  };

  // ─── Fechar Modal ───
  window.closeLeadModal = function () {
    var modal = document.getElementById('miModal');
    if (!modal) return;
    modal.classList.remove('mi-visible');
    document.body.style.overflow = '';
    setTimeout(function () { modal.style.display = 'none'; }, 250);
  };

  // ─── Navegação entre steps ───
  window.goToStep = function (step) {
    state.step = step;

    // Hide all step contents
    document.querySelectorAll('.mi-step-content').forEach(function (el) { el.style.display = 'none'; });

    // Show target step
    var stepId = step === 'noCoverage' ? 'miNoCoverage' : ('miStep' + step);
    var target = document.getElementById(stepId);
    if (target) target.style.display = '';

    // Update progress indicators
    document.querySelectorAll('.mi-step').forEach(function (el) {
      var s = parseInt(el.getAttribute('data-step'));
      el.classList.remove('active', 'completed');
      if (step === 'noCoverage') {
        if (s === 1) el.classList.add('completed');
      } else if (s < step) {
        el.classList.add('completed');
      } else if (s === step) {
        el.classList.add('active');
      }
    });

    // Update step lines
    document.querySelectorAll('.mi-step-line').forEach(function (el, i) {
      var lineStep = i + 1;
      el.classList.toggle('active', typeof step === 'number' && lineStep < step);
    });
  };

  // ─── Fechar com overlay/ESC ───
  document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'miModal') closeLeadModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLeadModal();
  });

  // ─── Máscara de CEP ───
  document.addEventListener('input', function (e) {
    if (e.target && e.target.id === 'mi_cep') {
      var v = e.target.value.replace(/\D/g, '');
      if (v.length > 8) v = v.slice(0, 8);
      if (v.length > 5) {
        e.target.value = v.slice(0, 5) + '-' + v.slice(5);
      } else {
        e.target.value = v;
      }
    }
  });

  // ─── Máscara de telefone ───
  document.addEventListener('input', function (e) {
    if (e.target && (e.target.id === 'mi_phone' || e.target.id === 'mi_wait_phone')) {
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

  // ─── STEP 1: Verificar Cobertura ───
  window.verificarCobertura = function () {
    var cepInput = document.getElementById('mi_cep');
    var cep = (cepInput.value || '').replace(/\D/g, '');

    if (cep.length !== 8) {
      showCepError('Informe um CEP válido com 8 dígitos.');
      return;
    }

    hideCepError();
    setCepLoading(true);

    // Esconder resultado anterior
    var addrResult = document.getElementById('miAddressResult');
    if (addrResult) addrResult.classList.add('mi-hidden');

    if (IS_WP) {
      // WordPress: chama via WP AJAX
      var formData = new FormData();
      formData.append('action', 'mi_viabilidade');
      formData.append('cep', cep);
      fetch(API_BASE, { method: 'POST', body: formData })
        .then(function (r) { return r.json(); })
        .then(handleViabilidadeResponse)
        .catch(handleViabilidadeError);
    } else {
      // Protótipo com PHP: consulta API de viabilidade (IXC real)
      fetch(API_BASE + 'viabilidade.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cep: cep })
      })
        .then(function (r) { return r.json(); })
        .then(handleViabilidadeResponse)
        .catch(handleViabilidadeError);
    }
  };

  function handleViabilidadeResponse(data) {
    setCepLoading(false);

    if (data.viavel) {
      state.endereco = data.endereco;
      state.cto = data.cto;

      var addrText = document.getElementById('miAddressText');
      var addrResult = document.getElementById('miAddressResult');
      if (addrText && data.endereco) {
        addrText.textContent = (data.endereco.logradouro || '') + ', ' + (data.endereco.bairro || '') + ' - ' + (data.endereco.cidade || '') + '/' + (data.endereco.uf || '');
      }
      if (addrResult) addrResult.classList.remove('mi-hidden');

      var confirmed = document.getElementById('miConfirmedAddress');
      if (confirmed && data.endereco) {
        confirmed.textContent = (data.endereco.bairro || '') + ', ' + (data.endereco.cidade || '') + '/' + (data.endereco.uf || '');
      }

      // Rastrear verificacao de cobertura com sucesso
      if (typeof window.miTrack === 'function') {
        window.miTrack('cep_check', { cep: (data.endereco && data.endereco.cep) || '', viable: true });
      }

      setTimeout(function () {
        goToStep(2);
        setTimeout(function () {
          var nameInput = document.getElementById('mi_name');
          if (nameInput) nameInput.focus();
        }, 300);
      }, 500);
    } else {
      if (data.sem_cobertura || data.sem_porta) {
        var msg = document.getElementById('miNoCoverageMsg');
        if (msg) msg.textContent = data.mensagem;
        state.endereco = data.endereco;
        if (typeof window.miTrack === 'function') window.miTrack('cep_check', { cep: (data.endereco && data.endereco.cep) || '', viable: false });
        goToStep('noCoverage');
      } else {
        showCepError(data.mensagem || 'Erro ao verificar cobertura.');
      }
    }
  }

  function handleViabilidadeError() {
    setCepLoading(false);
    showCepError('Erro de conexão. Tente novamente.');
  }

  // Enter no campo CEP submete
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target && e.target.id === 'mi_cep') {
      e.preventDefault();
      verificarCobertura();
    }
  });

  // ─── STEP 2: Submeter Lead ───
  window.submitLead = function (e) {
    e.preventDefault();

    var name = document.getElementById('mi_name').value.trim();
    var phone = document.getElementById('mi_phone').value.trim();
    var email = document.getElementById('mi_email').value.trim();
    var plan = document.getElementById('mi_plan').value;

    if (!name || !phone || !email) {
      showError('Preencha todos os campos.');
      return false;
    }

    var phoneDigits = phone.replace(/\D/g, '');
    if (phoneDigits.length < 10 || phoneDigits.length > 11) {
      showError('Informe um número de WhatsApp válido.');
      return false;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showError('Informe um e-mail válido.');
      return false;
    }

    hideError();
    setSubmitLoading(true);

    var leadData = {
      name: name,
      phone: phoneDigits,
      email: email,
      plan: plan,
      cep: state.endereco ? state.endereco.cep : '',
      bairro: state.endereco ? state.endereco.bairro : '',
      endereco: state.endereco ? (state.endereco.logradouro || '') : '',
    };

    if (IS_WP) {
      var formData = new FormData();
      formData.append('action', 'fazup_lead');
      formData.append('nonce', fazupCRM.nonce);
      Object.keys(leadData).forEach(function (k) { formData.append(k, leadData[k]); });

      fetch(API_BASE, { method: 'POST', body: formData })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          setSubmitLoading(false);
          if (data.success) {
            firePixel(plan);
            showSuccess(leadData);
          } else {
            showError(data.data?.message || 'Erro ao enviar. Tente novamente.');
          }
        })
        .catch(function () {
          setSubmitLoading(false);
          showError('Erro de conexão. Tente novamente.');
        });
    } else {
      // Grava o lead no CRM (best-effort) ANTES de seguir pro WhatsApp,
      // pra não perder o lead se o cliente desistir do hand-off do WhatsApp.
      var jornada = (typeof window.miJourneyText === 'function') ? window.miJourneyText() : '';
      miPostLead('pre-pedido-site', {
        nome: name,
        telefone: phoneDigits,
        email: email,
        observacao: 'Plano: ' + (plan || '—') + ' · CEP: ' + (leadData.cep || '—') +
                    ' · Bairro: ' + (leadData.bairro || '—') + ' · Endereço: ' + (leadData.endereco || '—'),
        jornada: jornada,
        origem: 'Pré-pedido site' + (plan ? ' — ' + plan : '')
      });
      setTimeout(function () {
        setSubmitLoading(false);
        firePixel(plan);
        showSuccess(leadData);
      }, 600);
    }

    return false;
  };

  // ─── Waitlist (sem cobertura) ───
  window.submitWaitlist = function (e) {
    e.preventDefault();

    var name = document.getElementById('mi_wait_name').value.trim();
    var phone = document.getElementById('mi_wait_phone').value.trim();
    var phoneDigits = phone.replace(/\D/g, '');

    if (!name || phoneDigits.length < 10) {
      showWaitError('Preencha nome e WhatsApp válido.');
      return false;
    }

    hideWaitError();
    setWaitLoading(true);

    if (typeof window.miTrack === 'function') {
      window.miTrack('waitlist_signup', { cep: state.endereco ? state.endereco.cep : '' });
    }

    var data = {
      name: name,
      phone: phoneDigits,
      cep: state.endereco ? state.endereco.cep : '',
      bairro: state.endereco ? state.endereco.bairro : '',
      waitlist: true,
    };

    // Grava o lead de espera no CRM (best-effort) antes de mostrar o sucesso.
    var jornada = (typeof window.miJourneyText === 'function') ? window.miJourneyText() : '';
    miPostLead('lista-espera-site', {
      nome: name,
      telefone: phoneDigits,
      observacao: 'SEM COBERTURA · CEP: ' + (data.cep || '—') + ' · Bairro: ' + (data.bairro || '—'),
      jornada: jornada,
      origem: 'Lista de espera (site)'
    });
    setTimeout(function () {
      setWaitLoading(false);
      console.log('[MasterInfo Waitlist]', data);

      // Mostra sucesso inline
      var noCov = document.getElementById('miNoCoverage');
      if (noCov) {
        noCov.innerHTML = '<div class="mi-success"><div class="mi-success-icon"><svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" class="mi-check-circle" stroke-width="2" fill="rgba(34,197,94,0.1)"/><path d="M20 33l8 8 16-16" class="mi-check-path" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Cadastro realizado!</h3><p>Vamos te avisar pelo WhatsApp<br>quando a fibra chegar no seu endereço.</p><button type="button" class="mi-close-text" onclick="closeLeadModal()">Fechar</button></div>';
      }
    }, 1200);

    return false;
  };

  // ─── Grava lead no backend (Bitrix via form-submit.php). Best-effort: nunca trava o fluxo. ───
  function miPostLead(form, data) {
    if (IS_WP) return; // no WP o lead já vai pela ação AJAX dedicada (submitLead)
    try {
      fetch(API_BASE + 'form-submit.php', {
        method: 'POST',
        keepalive: true,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ form: form, data: data })
      }).catch(function () {});
    } catch (e) {}
  }

  // ─── Sucesso → WhatsApp ───
  function showSuccess(leadData) {
    // Montar link WhatsApp com contexto
    var msg = 'Olá! Acabei de fazer um pré-pedido no site.\n';
    if (state.plan) msg += '📋 Plano: ' + state.plan + '\n';
    msg += '👤 Nome: ' + leadData.name + '\n';
    if (state.endereco) msg += '📍 Endereço: ' + (state.endereco.bairro || '') + ', ' + (state.endereco.cidade || '') + '\n';
    msg += '\nQuero finalizar minha contratação!';

    var whatsappLink = 'https://wa.me/5547989212991?text=' + encodeURIComponent(msg);
    var linkEl = document.getElementById('miWhatsappLink');
    if (linkEl) linkEl.href = whatsappLink;

    goToStep(3);
  }

  // ─── Helpers ───
  function showCepError(msg) {
    var el = document.getElementById('miCepError');
    if (el) { el.textContent = msg; el.style.display = ''; }
  }
  function hideCepError() {
    var el = document.getElementById('miCepError');
    if (el) el.style.display = 'none';
  }
  function setCepLoading(loading) {
    var btn = document.getElementById('miCepBtn');
    var text = document.getElementById('miCepBtnText');
    var spin = document.getElementById('miCepBtnLoading');
    if (btn) btn.disabled = loading;
    if (text) text.style.display = loading ? 'none' : '';
    if (spin) spin.style.display = loading ? 'inline-flex' : 'none';
  }

  function showError(msg) {
    var el = document.getElementById('miError');
    if (el) { el.textContent = msg; el.style.display = ''; }
  }
  function hideError() {
    var el = document.getElementById('miError');
    if (el) el.style.display = 'none';
  }
  function setSubmitLoading(loading) {
    var btn = document.getElementById('miSubmitBtn');
    var text = document.getElementById('miBtnText');
    var spin = document.getElementById('miBtnLoading');
    if (btn) btn.disabled = loading;
    if (text) text.style.display = loading ? 'none' : '';
    if (spin) spin.style.display = loading ? 'inline-flex' : 'none';
  }

  function showWaitError(msg) {
    var el = document.getElementById('miWaitError');
    if (el) { el.textContent = msg; el.style.display = ''; }
  }
  function hideWaitError() {
    var el = document.getElementById('miWaitError');
    if (el) el.style.display = 'none';
  }
  function setWaitLoading(loading) {
    var btn = document.getElementById('miWaitBtn');
    var text = document.getElementById('miWaitBtnText');
    var spin = document.getElementById('miWaitBtnLoading');
    if (btn) btn.disabled = loading;
    if (text) text.style.display = loading ? 'none' : '';
    if (spin) spin.style.display = loading ? 'inline-flex' : 'none';
  }

  function firePixel(plan) {
    // GA4 + Google Ads + Facebook Pixel (via tracking.js hub)
    if (typeof window.miTrack === 'function') {
      window.miTrack('generate_lead', {
        plan: plan || 'Site MasterInfo',
        value: 0,
        currency: 'BRL'
      });
    }
    // Fallback direto pro Facebook Pixel se tracking.js nao carregou
    else if (typeof fbq === 'function') {
      fbq('track', 'Lead', {
        content_name: plan || 'Site MasterInfo',
        content_category: 'Internet Fibra'
      });
    }
  }

})();
