// Array global para guardar os marcadores e usar na busca
const listaMarcadores = [];

// 1. Inicializa o Mapa em JF
const map = L.map('map', { zoomControl: false }).setView([-21.7664, -43.3496], 13);

// Reposiciona o botão de zoom
L.control.zoom({ position: 'bottomright' }).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

// 2. Consome o arquivo JSON
const versaoApp = new Date().getTime();

fetch(`bares_finais.json?v=${versaoApp}`)
    .then(response => response.json())
    .then(bares => {
        bares.forEach(bar => {
            if (bar.latitude && bar.longitude) {
                const marker = L.marker([bar.latitude, bar.longitude]).addTo(map);
                
                // Salva o nome do bar dentro do marcador
                marker.nomeDoBar = bar.nome;
                listaMarcadores.push(marker);

                const buscaExata = encodeURIComponent(bar.nome + ', ' + bar.endereco);
                const linkGoogleMaps = `https://www.google.com/maps/dir/?api=1&destination=${buscaExata}`;
                const linkUber = `https://m.uber.com/ul/?action=setPickup&pickup=my_location&dropoff[formatted_address]=${buscaExata}&dropoff[nickname]=${encodeURIComponent(bar.nome)}`;

                const balao = `
                    <div>
                        <img src="${bar.imagem}" alt="${bar.nome}" class="popup-img">
                        <h3 class="popup-title">${bar.nome}</h3>
                        <p class="popup-address">📍 ${bar.endereco}</p>
                        
                        <div class="box-prato">
                            <p class="nome-prato">🍽️ ${bar.prato}</p>
                            <p class="desc-prato">${bar.descricao_prato}</p>
                        </div>

                        <p class="info-extra"><strong>📞 Tel:</strong> ${bar.telefone}</p>
                        <p class="info-extra"><strong>🕒 Horário:</strong> ${bar.horario}</p>

                        <div class="area-botoes">
                            <a href="${linkGoogleMaps}" target="_blank" class="btn btn-google">🗺️ Google Maps</a>
                            <a href="${linkUber}" target="_blank" class="btn btn-uber">🚗 Chamar Uber</a>
                        </div>
                    </div>
                `;

                marker.bindPopup(balao);
            }
        });
    })
    .catch(erro => console.error("Erro ao carregar o mapa:", erro));

// --- LÓGICA DE INTERFACE E PWA ---

// Função ninja para ignorar acentos
function removerAcentos(texto) {
    return texto.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
}

// Função de busca atualizada
function buscarBar() {
    const inputOriginal = document.getElementById('search-input').value.toLowerCase();
    const termoBusca = removerAcentos(inputOriginal);
    
    listaMarcadores.forEach(m => {
        const nomeOriginal = m.nomeDoBar.toLowerCase();
        const nomeLimpo = removerAcentos(nomeOriginal);

        if (nomeLimpo.includes(termoBusca) && termoBusca !== "") {
            
            const zoomIn = 17;
            
            // 1. Pega a coordenada do bar e converte para "Pixels" na tela
            const pontoEmPixels = map.project(m.getLatLng(), zoomIn);
            
            // 2. A Mágica: Subtraímos 150 pixels no eixo Y (Isso faz a câmera olhar mais para cima, 
            // e consequentemente o pino e o balão descem para o meio da visão livre da tela)
            pontoEmPixels.y -= 150;
            
            // 3. Converte os pixels de volta para coordenada e manda o mapa voar pra lá
            map.setView(map.unproject(pontoEmPixels, zoomIn), zoomIn);
            
            // 4. Abre o balão suavemente no novo centro perfeito
            m.openPopup();
        }
    });
}

// Dropdown Menu
function toggleMenu() {
    const menu = document.getElementById('menu');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
}

// Esconde o menu se clicar fora dele no mapa
map.on('click', function() {
    document.getElementById('menu').style.display = 'none';
});

// Compartilhar WhatsApp
function shareApp() {
    const text = "Partiu Comida di Buteco JF! 🍻 Dá uma olhada nesse mapa para roteirizar os bares: " + window.location.href;
    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`, '_blank');
}

// Lógica de PWA (Instalação)
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
});

function installApp() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then((choiceResult) => {
            deferredPrompt = null;
        });
    } else {
        alert("Para instalar: \n\nNo Android (Chrome): Clique nos 3 pontinhos > Adicionar a Tela Inicial. \n\nNo iPhone (Safari): Clique em Compartilhar > Adicionar à Tela de Início.");
    }
    toggleMenu();
}

// --- GEOLOCALIZAÇÃO ---
if ("geolocation" in navigator) {
    const iconeUsuario = L.divIcon({
        className: 'user-location-icon',
        html: '<div style="background-color: #3498db; width: 15px; height: 15px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.5); animation: pulse 2s infinite;"></div>',
        iconSize: [21, 21]
    });

    let marcadorUsuario = null;

    navigator.geolocation.watchPosition((pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        if (marcadorUsuario) {
            marcadorUsuario.setLatLng([lat, lon]);
        } else {
            marcadorUsuario = L.marker([lat, lon], { icon: iconeUsuario }).addTo(map);
            marcadorUsuario.bindPopup("Você está aqui! 🍺");
            map.setView([lat, lon], 15);
        }
    }, (erro) => {
        console.error("Erro ao capturar localização:", erro);
    }, {
        enableHighAccuracy: true
    });
}