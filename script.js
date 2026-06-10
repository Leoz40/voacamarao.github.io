(function () {
  'use strict';

  /* =============================================
     FAQ Accordion
     ============================================= */
  function initFaq() {
    const items = document.querySelectorAll('.faq-item');
    items.forEach(function (item) {
      const question = item.querySelector('.faq-question');
      question.addEventListener('click', function () {
        const isActive = item.classList.contains('active');
        items.forEach(function (el) { el.classList.remove('active'); });
        if (!isActive) { item.classList.add('active'); }
      });
    });
  }

  /* =============================================
     Form Lead Capture
     ============================================= */
  function initForm() {
    const form = document.getElementById('leadForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const nome = document.getElementById('nome').value.trim();
      const empresa = document.getElementById('empresa').value.trim();
      const estimativa = document.getElementById('estimativa').value;

      if (!nome || !empresa || !estimativa) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
      }

      const mensagem =
        'Olá! Meu nome é ' +
        encodeURIComponent(nome) +
        ', represento a empresa ' +
        encodeURIComponent(empresa) +
        '. Tenho interesse em um fornecimento de aproximadamente ' +
        encodeURIComponent(estimativa) +
        ' de camarão seco por mês. Podemos falar sobre a tabela de preços no atacado?';

      /* ---- Envio para backend (API) ---- */
      fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: nome, empresa: empresa, estimativa: estimativa })
      }).catch(function () {
        /* Se o backend não estiver rodando, falha silenciosa — segue para WhatsApp */
      });

      /* ---- Redirecionamento para WhatsApp ---- */
      var telefone = '5585991057995'; /* substituir pelo número real */
      var url = 'https://api.whatsapp.com/send?phone=' + telefone + '&text=' + mensagem;
      window.open(url, '_blank');
    });
  }

  /* =============================================
     Init
     ============================================= */
  document.addEventListener('DOMContentLoaded', function () {
    initFaq();
    initForm();
  });
})();
