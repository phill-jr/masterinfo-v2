const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const loader = fs.readFileSync(path.join(root, 'site-loader.js'), 'utf8');
const checkout = fs.readFileSync(path.join(root, 'checkout.js'), 'utf8');
const plans = JSON.parse(fs.readFileSync(path.join(root, 'config.json'), 'utf8')).planos;
const source = loader.slice(loader.indexOf('  function loadPromoBar('), loader.indexOf('  function loadPlanos('));
const format = loader.match(/  function formatBRL\(n\) \{[^}]+\}/)[0];
let checks = 0;
function check(name, fn) { fn(); checks++; console.log('OK ' + name); }
function render(planList, planId = 'lite-basic') {
  const offer = { textContent: 'Confira nossos planos de internet' };
  const note = { textContent: 'Consulte a cobertura' };
  const link = { textContent: 'Ver planos', attrs: { href: '#planos' }, setAttribute(k, v) { this.attrs[k] = v; } };
  const bar = { getAttribute: () => planId, querySelector: s => ({ '.promo-bar-offer': offer, '.promo-bar-cta-text': note, '.promo-bar-btn': link })[s] };
  const context = { document: { getElementById: () => bar }, plans: planList };
  vm.runInNewContext(source + format + '\nloadPromoBar(plans);', context);
  return { offer: offer.textContent, note: note.textContent, ...link };
}
check('oferta usa preco pontual do cadastro', () => assert.equal(render(plans).offer, '1000 Mega por R$ 119,00/mês pagando em dia'));
check('sem app de TV quando categorias estao vazias', () => assert.equal(render(plans).note, 'Sem app de TV incluso'));
check('CTA seleciona o mesmo plano anunciado', () => assert.equal(render(plans).attrs.href, 'checkout.html?plano=lite-basic'));
check('convencao declarativa mantida', () => assert.equal(render(plans).attrs['data-plano'], 'lite-basic'));
check('mudanca no admin atualiza preco sem editar HTML', () => assert.match(render([{ ...plans.find(p => p.id === 'lite-basic'), precoPontual: 127.95 }]).offer, /127,95/));
check('plano removido mantem fallback neutro', () => assert.equal(render([]).attrs.href, '#planos'));
check('cadastro ausente mantem fallback neutro', () => assert.equal(render(undefined).offer, 'Confira nossos planos de internet'));
for (const value of [null, 0, -5, 'gratis', Infinity, NaN]) {
  check('preco invalido nao vira oferta: ' + String(value), () => {
    const result = render([{ id: 'lite-basic', velocidade: '1000', unidade: 'Mega', precoPontual: value }]);
    assert.equal(result.attrs.href, '#planos');
  });
}
check('preco cheio nao promete desconto inexistente', () => {
  const result = render([{ id: 'lite-basic', velocidade: '1000', unidade: 'Mega', precoCheio: 129 }]);
  assert.equal(result.offer, '1000 Mega por R$ 129,00/mês');
});
check('beneficio desconhecido nao inventa app gratis', () => {
  const result = render([{ id: 'lite-basic', velocidade: '1000', unidade: 'Mega', precoCheio: 129, categorias: ['advanced'] }]);
  assert.equal(result.note, 'Confira os benefícios do plano');
});
check('id do cadastro e codificado no link', () => {
  const id = 'plano&extra=1';
  assert.equal(render([{ id, velocidade: '1000', unidade: 'Mega', precoCheio: 129 }], id).attrs.href, 'checkout.html?plano=plano%26extra%3D1');
});
for (const home of ['index.html', 'index-light.html']) {
  const html = fs.readFileSync(path.join(root, home), 'utf8');
  check(home + ': fallback nao anuncia oferta antiga', () => {
    const bar = html.slice(html.indexOf('id="promoBar"'), html.indexOf('id="promoBarClose"'));
    assert.doesNotMatch(bar, /119,90|SKY ou Deezer|plano=1000|OFERTA DO MÊS/);
    assert.match(bar, /data-promo-plano="lite-basic"/);
    assert.match(bar, /href="#planos"/);
  });
  check(home + ': cache do loader renovado', () => assert.match(html, /site-loader\.js\?v=20260906-oferta/));
}
check('aliases de checkout apontam para planos existentes', () => {
  const aliases = vm.runInNewContext('(' + checkout.match(/var PLAN_ALIASES = (\{[^}]+\})/)[1] + ')');
  for (const id of Object.values(aliases)) assert.ok(plans.some(p => p.id === id), id);
  assert.equal(aliases['800'], 'lite-premium');
  assert.equal(aliases['1000'], 'lite-basic');
});
check('checkout nao garante instalacao em 24h', () => assert.doesNotMatch(fs.readFileSync(path.join(root, 'checkout.html'), 'utf8'), /Instala[cç][aã]o 24h/i));
check('familia nao promete Wi-Fi 6 na linha Lite', () => {
  const html = fs.readFileSync(path.join(root, 'familia/index.html'), 'utf8');
  assert.doesNotMatch(html, /A partir de 800 Mega, os planos.*Wi-Fi 6/);
  assert.match(html, /linha Lite, o plano inclui 1 roteador e não inclui Wi-Fi 6/);
});
console.log(checks + ' verificacoes passaram. Sem chamadas externas ou envio de leads.');
