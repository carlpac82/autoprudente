// ╔════════════════════════════════════════════════════════════════════════════╗
// ║  TEMPLATE CHECK-IN AEROPORTO DE FARO                                       ║
// ║  Template único com instruções de check-in e ponto de encontro             ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Cole este código no Console (F12) do browser na página Admin → WhatsApp

const templateCheckIn = {
    name: "checkin_faro_airport",
    category: "UTILITY",
    content_pt: `Exmo. Cliente,

A Auto Prudente Rent a Car é a empresa responsável pela entrega da sua viatura no Aeroporto de Faro.

Para agilizar o processo de entrega, agradecemos que nos indique o seu número de voo, o seu endereço de e-mail e, se possível, efetue o check-in online através do seguinte link:
👉 https://auto-prudente.com/en/online-checkin/

O ponto de encontro é na zona das Chegadas do Aeroporto de Faro, junto à Saída D, em frente ao Café Central, onde um dos nossos colegas estará à sua espera com um cartaz com a indicação:
"Auto Prudente / Abbycar".

Pedimos, por favor, que aguarde no ponto de encontro.

Com os melhores cumprimentos,
Auto Prudente Rent a Car`,

    content_en: `Dear Customer,

Auto Prudente Rent a Car is the company responsible for delivering your vehicle at Faro Airport.

To speed up the delivery process, we kindly ask you to provide us with your flight number, your email address, and, if possible, complete the online check-in at:
👉 https://auto-prudente.com/en/online-checkin/

The meeting point is in the Arrivals area of Faro Airport, next to Exit D, in front of Café Central, where one of our colleagues will be waiting for you with a sign that reads:
"Auto Prudente / Abbycar".

Please wait at the meeting point.

Best regards,
Auto Prudente Rent a Car`,

    content_fr: `Cher Client,

Auto Prudente Rent a Car est l'entreprise responsable de la livraison de votre véhicule à l'aéroport de Faro.

Afin d'accélérer le processus de livraison, nous vous prions de bien vouloir nous communiquer votre numéro de vol, votre adresse e-mail et, si possible, d'effectuer l'enregistrement en ligne via le lien suivant :
👉 https://auto-prudente.com/en/online-checkin/

Le point de rencontre se situe dans la zone des Arrivées de l'aéroport de Faro, à la sortie D, en face du Café Central, où l'un de nos collègues vous attendra avec une pancarte indiquant :
"Auto Prudente / Abbycar".

Merci de bien vouloir patienter à ce point de rencontre.

Cordialement,
Auto Prudente Rent a Car`,

    content_de: `Sehr geehrter Kunde,

Auto Prudente Rent a Car ist das Unternehmen, das für die Übergabe Ihres Fahrzeugs am Flughafen Faro verantwortlich ist.

Um den Übergabeprozess zu beschleunigen, bitten wir Sie, uns Ihre Flugnummer und E-Mail-Adresse mitzuteilen und, wenn möglich, den Online-Check-in unter folgendem Link durchzuführen:
👉 https://auto-prudente.com/en/online-checkin/

Der Treffpunkt befindet sich im Ankunftsbereich des Flughafens Faro, neben Ausgang D, gegenüber dem Café Central, wo einer unserer Mitarbeiter mit einem Schild mit der Aufschrift
„Auto Prudente / Abbycar" auf Sie warten wird.

Bitte warten Sie am Treffpunkt.

Mit freundlichen Grüßen
Auto Prudente Rent a Car`
};

// Expandir para todos os idiomas (1 idioma por template)
const languageCodes = {
    pt_PT: 'content_pt',
    en: 'content_en',
    fr: 'content_fr',
    de: 'content_de'
};

const templates = [];
Object.entries(languageCodes).forEach(([langCode, contentKey]) => {
    templates.push({
        name: templateCheckIn.name,
        category: templateCheckIn.category,
        language_code: langCode,
        [`content_${langCode.split('_')[0]}`]: templateCheckIn[contentKey],
        // Enviar apenas o conteúdo do idioma específico
        content_pt: langCode === 'pt_PT' ? templateCheckIn.content_pt : '',
        content_en: langCode === 'en' ? templateCheckIn.content_en : '',
        content_fr: langCode === 'fr' ? templateCheckIn.content_fr : '',
        content_de: langCode === 'de' ? templateCheckIn.content_de : ''
    });
});

// ════════════════════════════════════════════════════════════════════════════
// FUNÇÕES
// ════════════════════════════════════════════════════════════════════════════

async function criarTemplateCheckIn() {
    console.log('🚀 Criando TEMPLATE CHECK-IN AEROPORTO...\n');
    
    let successCount = 0;
    let errorCount = 0;
    
    for (const template of templates) {
        try {
            const response = await fetch('/api/whatsapp/templates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify(template)
            });
            
            const result = await response.json();
            
            if (result.ok) {
                console.log(`✅ ${template.name} (${template.language_code}) - CRIADO E ENVIADO`);
                successCount++;
            } else {
                console.log(`❌ ${template.name} (${template.language_code}) - ERRO: ${result.error}`);
                errorCount++;
            }
            
            // Aguardar 1 segundo entre cada criação
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.log(`❌ ${template.name} (${template.language_code}) - ERRO: ${error.message}`);
            errorCount++;
        }
    }
    
    console.log(`\n╔════════════════════════════════════╗`);
    console.log(`║   RESUMO - TEMPLATE CHECK-IN       ║`);
    console.log(`╠════════════════════════════════════╣`);
    console.log(`║ ✅ Criados: ${successCount.toString().padStart(2)}                     ║`);
    console.log(`║ ❌ Erros:   ${errorCount.toString().padStart(2)}                     ║`);
    console.log(`║ 📊 Total:    4                     ║`);
    console.log(`╚════════════════════════════════════╝`);
    
    console.log('\n⏰ Aguarde até 24 horas para aprovação do WhatsApp.');
    console.log('💡 Depois de aprovado, use o botão ✈️ no chat para enviar!');
}

async function verificarTemplateCheckIn() {
    await fetch('/api/whatsapp/templates/sync-status', {
        method: 'POST',
        credentials: 'same-origin'
    });
    
    const data = await fetch('/api/whatsapp/templates')
        .then(r => r.json());
    
    const checkInTemplates = data.templates.filter(t => t.name === 'checkin_faro_airport');
    
    console.log('\n✈️ STATUS TEMPLATE CHECK-IN AEROPORTO:\n');
    
    checkInTemplates.forEach(t => {
        const statusIcon = t.status === 'APPROVED' ? '✅' : 
                          t.status === 'PENDING' ? '⏳' : '❌';
        console.log(`${statusIcon} ${t.language_code.toUpperCase()}: ${t.status}`);
    });
    
    const approved = checkInTemplates.filter(t => t.status === 'APPROVED').length;
    console.log(`\n📊 ${approved}/4 idiomas aprovados`);
    
    if (approved === 4) {
        console.log('\n🎉 TODOS OS IDIOMAS APROVADOS!');
        console.log('✅ Pode usar o botão ✈️ no WhatsApp Dashboard!');
    }
}

// ════════════════════════════════════════════════════════════════════════════
// MENSAGEM INICIAL
// ════════════════════════════════════════════════════════════════════════════

console.log('%c╔════════════════════════════════════════════════════════════╗', 'color: #0084FF; font-weight: bold');
console.log('%c║        TEMPLATE CHECK-IN AEROPORTO DE FARO                ║', 'color: #0084FF; font-weight: bold');
console.log('%c║        4 idiomas: PT, EN, FR, DE                          ║', 'color: #0084FF; font-weight: bold');
console.log('%c╚════════════════════════════════════════════════════════════╝', 'color: #0084FF; font-weight: bold');
console.log('\n✈️ Template único para check-in no Aeroporto de Faro');
console.log('📋 Inclui:');
console.log('   • Número de voo e email');
console.log('   • Link check-in online');
console.log('   • Ponto de encontro (Saída D, Café Central)');
console.log('   • Placa "Auto Prudente / Abbycar"');
console.log('\n🚀 Para criar o template (4 idiomas):');
console.log('%c   criarTemplateCheckIn()', 'color: yellow; font-weight: bold; font-size: 14px');
console.log('\n💡 Para verificar status depois:');
console.log('%c   verificarTemplateCheckIn()', 'color: cyan; font-weight: bold');
