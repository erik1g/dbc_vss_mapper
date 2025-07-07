document.addEventListener('DOMContentLoaded', () => {
  console.log('Mapping Editor gestartet.');

    const vssEl = document.getElementById('vssDataJSON');
    const dbcEl = document.getElementById('dbcDataJSON');

    const vssDataRaw = vssEl ? JSON.parse(vssEl.textContent) : {};
    const dbcDataRaw = dbcEl ? JSON.parse(dbcEl.textContent) : {};

    console.log(vssDataRaw, dbcDataRaw);
  //------------------------------------------
  // 2️⃣ VSS-Signale extrahieren (rekursiv)
  //------------------------------------------
  function extractVssSignals(node, prefix = '') {
    let results = [];
    if (!node || !node.children) return results;

    for (const [key, value] of Object.entries(node.children)) {
      const path = prefix ? `${prefix}.${key}` : key;
      if (value.type !== 'branch') {
        results.push(path);
      } else {
        results = results.concat(extractVssSignals(value, path));
      }
    }

    return results;
  }

  const vssSignalList = extractVssSignals(vssDataRaw?.Vehicle || {});
  console.log('VSS Signale:', vssSignalList);

  //------------------------------------------
  // 3️⃣ DBC-Signale extrahieren
  //------------------------------------------
  function extractDbcSignals(dbcData) {
    const list = [];
    if (!dbcData || !dbcData.messages) return list;

    dbcData.messages.forEach(msg => {
      if (msg.signals) {
        msg.signals.forEach(sig => {
          list.push({
            message: msg.message_name,
            signal: sig.signal_name
          });
        });
      }
    });

    return list;
  }

  const dbcSignalList = extractDbcSignals(dbcDataRaw);
  console.log('DBC Signale:', dbcSignalList);

  //------------------------------------------
  // 4️⃣ Select-Dropdowns befüllen
  //------------------------------------------
  function fillSelect(selectId, options, formatter) {
    const select = document.getElementById(selectId);
    select.innerHTML = '';
    options.forEach(opt => {
      const option = document.createElement('option');
      option.value = JSON.stringify(opt);
      option.textContent = formatter(opt);
      select.appendChild(option);
    });
  }

  fillSelect('vss-select', vssSignalList, (s) => s);
  fillSelect('dbc-select', dbcSignalList, (s) => `${s.message}.${s.signal}`);

  //------------------------------------------
  // 5️⃣ Mapping-Logik
  //------------------------------------------
  let mapping = [];

  // Existierendes Mapping laden
  if (window.existingMapping) {
    mapping = window.existingMapping;
    console.log('Vorhandenes Mapping geladen:', mapping);
  }

  function renderMapping() {
    const list = document.getElementById('mapping-list');
    list.innerHTML = '';

    if (mapping.length === 0) {
      const empty = document.createElement('li');
      empty.textContent = 'Noch keine Mappings vorhanden.';
      list.appendChild(empty);
    } else {
      mapping.forEach((item, idx) => {
        const li = document.createElement('li');
        li.textContent = `${item.vss_signal} ↔ ${item.dbc_message}.${item.dbc_signal}`;

        const delBtn = document.createElement('button');
        delBtn.textContent = 'Entfernen';
        delBtn.onclick = () => {
          mapping.splice(idx, 1);
          renderMapping();
        };

        li.appendChild(delBtn);
        list.appendChild(li);
      });
    }

    document.getElementById('mapping-input').value = JSON.stringify(mapping, null, 2);
  }

  document.getElementById('add-mapping-btn').addEventListener('click', () => {
    const vssSelected = JSON.parse(document.getElementById('vss-select').value);
    const dbcSelected = JSON.parse(document.getElementById('dbc-select').value);

    if (!vssSelected || !dbcSelected) {
      alert('Bitte sowohl ein VSS- als auch ein DBC-Signal auswählen!');
      return;
    }

    mapping.push({
      vss_signal: vssSelected,
      dbc_message: dbcSelected.message,
      dbc_signal: dbcSelected.signal,
      transform: { mapping: [] }
    });

    renderMapping();
  });

  renderMapping();
});

