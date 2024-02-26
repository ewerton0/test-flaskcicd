function uploadFiles() {
    var form = document.getElementById("upload-form");
    var formData = new FormData(form);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error("Error:", error));
}

function displayFileName() {
    var fileInput = document.getElementById("file-upload");
    var fileNameDisplay = document.getElementById("selected-file-name");
    if (fileInput.files.length > 0) {
        var fileNames = [];
        for (var i = 0; i < fileInput.files.length; i++) {
            fileNames.push(fileInput.files[i].name);
        }
        fileNameDisplay.textContent = fileNames.join(", ");
    } else {
        fileNameDisplay.textContent = "No file selected";
    }
}

function displayResults(results) {
    var resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    // Objeto para armazenar os resultados agrupados por arquivo
    var groupedResults = {};

    results.forEach((result) => {
        // Verifica se o arquivo já está no objeto agrupado
        if (!(result.fileName in groupedResults)) {
            // Inicializa o objeto para este arquivo
            groupedResults[result.fileName] = {
                containsKeyPhrase: false, // Flag para verificar se já há uma página com containsKeyPhrase
                hasLowQuality: false, // Flag para verificar se há uma página com qualidade baixa
                result: null // Resultado a ser exibido
            };
        }

        // Verifica se esta página contém a chave
        if (result.containsKeyPhrase) {
            // Define a flag para este arquivo como true
            groupedResults[result.fileName].containsKeyPhrase = true;
            // Atualiza o resultado para esta página
            groupedResults[result.fileName].result = result;
        } else if (!groupedResults[result.fileName].containsKeyPhrase) {
            // Se esta página não contiver a chave e ainda não tiver sido definido um resultado para este arquivo,
            // atualiza o resultado para esta página
            groupedResults[result.fileName].result = result;
        }

        // Verifica se há uma página com qualidade baixa
        if (result.isQualityLow) {
            // Define a flag para este arquivo como true
            groupedResults[result.fileName].hasLowQuality = true;
        }
    });

    // Adiciona os resultados agrupados à página
    Object.keys(groupedResults).forEach((fileName) => {
        var result = groupedResults[fileName].result;
        var containsKeyPhrase = groupedResults[fileName].result.containsKeyPhrase ? 'Sim' : 'Não';
        var isQualityLow = groupedResults[fileName].result.isQualityLow ? 'Sim' : 'Não';

        var resultElement = document.createElement("div");
        resultElement.innerHTML = `<p>Image: ${result.fileName}</p>
                                <p>Possui proteção total?: ${containsKeyPhrase}</p>
                                <p>Reserva: ${result.codigoReserva}</p>
                                <p>Qualidade baixa? : ${isQualityLow}</p>
                                <hr>`;
        resultsContainer.appendChild(resultElement);
    });
}
