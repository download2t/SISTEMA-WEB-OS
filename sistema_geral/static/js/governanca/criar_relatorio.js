document.addEventListener("DOMContentLoaded", function () {
  const itensContainer = document.getElementById("itens-container");
  const itemTemplate = document.getElementById("item-template").content;
  const adicionarItemBtn = document.getElementById("adicionar-item");
  const itensLavanderiaData = document.getElementById("itens-lavanderia-data");

  // Função para adicionar um novo item
  function adicionarItem(itemData = {}) {
    const newItem = document.importNode(itemTemplate, true);
    const select = newItem.querySelector('select[name="item_lavanderia"]');
    const qtdItens = newItem.querySelector('input[name="qtd_itens"]');
    const qtdRelavagens = newItem.querySelector('input[name="qtd_relavagens"]');
    const removerItemBtn = newItem.querySelector(".remover-item");

    if (itemData.item_lavanderia) {
      select.value = itemData.item_lavanderia;
    }
    if (itemData.qtd_itens) {
      qtdItens.value = itemData.qtd_itens;
    }
    if (itemData.qtd_relavagens) {
      qtdRelavagens.value = itemData.qtd_relavagens;
    }

    removerItemBtn.addEventListener("click", function () {
      newItem.remove();
      atualizarDadosItens();
    });

    itensContainer.appendChild(newItem);
    atualizarDadosItens();
  }

  // Remove um item do container
  itensContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("remover-item")) {
      event.target.closest(".item").remove();
    }
  });

  // Função para atualizar os dados dos itens no campo oculto
  function atualizarDadosItens() {
    const itens = [];
    itensContainer.querySelectorAll(".item").forEach((item) => {
      const itemData = {
        item_lavanderia: item.querySelector('select[name="item_lavanderia"]')
          .value,
        qtd_itens: item.querySelector('input[name="qtd_itens"]').value,
        qtd_relavagens: item.querySelector('input[name="qtd_relavagens"]')
          .value,
      };
      itens.push(itemData);
    });
    itensLavanderiaData.value = JSON.stringify(itens);
  }

  // Adicionar um item inicial se houver dados no campo oculto
  if (itensLavanderiaData.value) {
    const itens = JSON.parse(itensLavanderiaData.value);
    itens.forEach((item) => adicionarItem(item));
  }

  // Adicionar um novo item ao clicar no botão
  adicionarItemBtn.addEventListener("click", function () {
    adicionarItem();
  });

  // Atualizar os dados dos itens sempre que houver uma mudança
  itensContainer.addEventListener("change", atualizarDadosItens);

  // Formatar campos de moeda e peso automaticamente
  function formatarCampo(input) {
    input.addEventListener("input", function (e) {
      let value = this.value.replace(/\D/g, ""); // Remove caracteres não numéricos
      value = (parseFloat(value) / 100).toFixed(2).replace(",", "."); // Adiciona casas decimais e formata para brasileiro
      this.value = value;
    });
  }

  document
    .querySelectorAll("#id_vrTotal, #id_pesoTotal")
    .forEach(formatarCampo);
});
