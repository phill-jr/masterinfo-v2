/**
 * MasterInfo — Banco de leads da pré-venda da Copa
 * Cole este código no Apps Script da sua planilha Google.
 * (Veja o passo a passo em COMO-ATIVAR-BANCO.md)
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000); // evita 2 gravações ao mesmo tempo

  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Cria o cabeçalho na primeira vez
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Data/Hora', 'Nome', 'Bairro', 'WhatsApp', 'Plano', 'Origem']);
    }

    var data = JSON.parse(e.postData.contents);

    sheet.appendRow([
      new Date(),
      data.nome || '',
      data.bairro || '',
      data.telefone || '',
      data.plano || '',
      data.origem || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ result: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ result: 'erro', message: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// Teste opcional: rode esta função uma vez pra checar se grava na planilha
function testar() {
  var fake = { postData: { contents: JSON.stringify({
    nome: 'Teste da Silva', bairro: 'Comasa', telefone: '(47) 99999-9999',
    plano: 'Plano da Copa', origem: 'teste'
  }) } };
  doPost(fake);
}
