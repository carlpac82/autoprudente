// ╔════════════════════════════════════════════════════════════════════════════╗
// ║  TEMPLATES WHATSAPP - MENSAGENS PARA INICIAR CONVERSAS                     ║
// ║  Precisam aprovação do WhatsApp (24h)                                      ║
// ║  Usados para contactar clientes FORA da janela de 24 horas                ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Cole este código no Console (F12) do browser na página Admin → WhatsApp

const templatesNegocio = [
    {
        name: "confirmacao_interesse",
        category: "UTILITY",
        content_pt: "Olá! Obrigado pelo seu interesse na Auto Prudente. Tem alguma dúvida sobre aluguer de veículos? Estamos aqui para ajudar!",
        content_en: "Hello! Thank you for your interest in Auto Prudente. Do you have any questions about vehicle rental? We're here to help!",
        content_fr: "Bonjour! Merci pour votre intérêt pour Auto Prudente. Avez-vous des questions sur la location de véhicules? Nous sommes là pour vous aider!",
        content_de: "Hallo! Vielen Dank für Ihr Interesse an Auto Prudente. Haben Sie Fragen zur Fahrzeugmiete? Wir sind hier um zu helfen!"
    },
    {
        name: "confirmacao_reserva",
        category: "UTILITY",
        content_pt: "✅ Reserva confirmada!\n\nVeículo reservado com sucesso. Receberá em breve todos os detalhes por email. Obrigado por escolher a Auto Prudente!",
        content_en: "✅ Booking confirmed!\n\nVehicle successfully reserved. You will receive all details by email shortly. Thank you for choosing Auto Prudente!",
        content_fr: "✅ Réservation confirmée!\n\nVéhicule réservé avec succès. Vous recevrez tous les détails par email sous peu. Merci d'avoir choisi Auto Prudente!",
        content_de: "✅ Buchung bestätigt!\n\nFahrzeug erfolgreich reserviert. Sie erhalten in Kürze alle Details per E-Mail. Vielen Dank, dass Sie sich für Auto Prudente entschieden haben!"
    },
    {
        name: "lembrete_recolha",
        category: "UTILITY",
        content_pt: "🚗 Lembrete de Recolha\n\nSua recolha do veículo está marcada para amanhã. Por favor confirme sua presença. Obrigado!",
        content_en: "🚗 Pick-up Reminder\n\nYour vehicle pick-up is scheduled for tomorrow. Please confirm your attendance. Thank you!",
        content_fr: "🚗 Rappel de Récupération\n\nVotre récupération du véhicule est prévue pour demain. Veuillez confirmer votre présence. Merci!",
        content_de: "🚗 Abholungs-Erinnerung\n\nIhre Fahrzeugabholung ist für morgen geplant. Bitte bestätigen Sie Ihre Anwesenheit. Danke!"
    },
    {
        name: "instrucoes_checkin",
        category: "UTILITY",
        content_pt: "📋 Instruções de Check-in\n\nPor favor traga:\n• Carta de condução válida\n• Cartão de crédito\n• Documento de identificação\n\nNos vemos em breve!",
        content_en: "📋 Check-in Instructions\n\nPlease bring:\n• Valid driver's license\n• Credit card\n• ID document\n\nSee you soon!",
        content_fr: "📋 Instructions d'Enregistrement\n\nVeuillez apporter:\n• Permis de conduire valide\n• Carte de crédit\n• Document d'identité\n\nÀ bientôt!",
        content_de: "📋 Check-in Anweisungen\n\nBitte mitbringen:\n• Gültiger Führerschein\n• Kreditkarte\n• Ausweisdokument\n\nBis bald!"
    },
    {
        name: "verificacao_devolucao",
        category: "UTILITY",
        content_pt: "🔄 Verificação de Devolução\n\nLembramos que a devolução do veículo está prevista para amanhã. Por favor confirme o horário. Obrigado pela preferência!",
        content_en: "🔄 Return Check\n\nWe remind you that the vehicle return is scheduled for tomorrow. Please confirm the time. Thank you for your preference!",
        content_fr: "🔄 Vérification du Retour\n\nNous vous rappelons que le retour du véhicule est prévu pour demain. Veuillez confirmer l'heure. Merci pour votre préférence!",
        content_de: "🔄 Rückgabe-Überprüfung\n\nWir erinnern Sie daran, dass die Fahrzeugrückgabe für morgen geplant ist. Bitte bestätigen Sie die Uhrzeit. Vielen Dank für Ihre Präferenz!"
    },
    {
        name: "agradecimento_servico",
        category: "UTILITY",
        content_pt: "🙏 Obrigado!\n\nObrigado por escolher a Auto Prudente. Esperamos que tenha tido uma excelente experiência. Até breve!",
        content_en: "🙏 Thank you!\n\nThank you for choosing Auto Prudente. We hope you had an excellent experience. See you soon!",
        content_fr: "🙏 Merci!\n\nMerci d'avoir choisi Auto Prudente. Nous espérons que vous avez eu une excellente expérience. À bientôt!",
        content_de: "🙏 Danke!\n\nVielen Dank, dass Sie sich für Auto Prudente entschieden haben. Wir hoffen, Sie hatten eine ausgezeichnete Erfahrung. Bis bald!"
    },
    {
        name: "seguimento_orcamento",
        category: "UTILITY",
        content_pt: "💰 Seguimento de Orçamento\n\nJá recebeu o nosso orçamento? Tem alguma dúvida? Estamos à disposição para ajudar!",
        content_en: "💰 Quote Follow-up\n\nHave you received our quote? Do you have any questions? We're available to help!",
        content_fr: "💰 Suivi du Devis\n\nAvez-vous reçu notre devis? Avez-vous des questions? Nous sommes disponibles pour vous aider!",
        content_de: "💰 Angebots-Nachverfolgung\n\nHaben Sie unser Angebot erhalten? Haben Sie Fragen? Wir stehen Ihnen gerne zur Verfügung!"
    },
    {
        name: "disponibilidade_veiculos",
        category: "UTILITY",
        content_pt: "🚙 Disponibilidade de Veículos\n\nTemos vários veículos disponíveis para as suas datas. Gostaria de saber mais sobre algum modelo em particular?",
        content_en: "🚙 Vehicle Availability\n\nWe have several vehicles available for your dates. Would you like to know more about any particular model?",
        content_fr: "🚙 Disponibilité des Véhicules\n\nNous avons plusieurs véhicules disponibles pour vos dates. Souhaitez-vous en savoir plus sur un modèle particulier?",
        content_de: "🚙 Fahrzeugverfügbarkeit\n\nWir haben mehrere Fahrzeuge für Ihre Termine verfügbar. Möchten Sie mehr über ein bestimmtes Modell erfahren?"
    },
    {
        name: "alteracao_reserva",
        category: "UTILITY",
        content_pt: "📝 Alteração de Reserva\n\nRecebemos o seu pedido de alteração. Estamos a processar e entraremos em contacto em breve. Obrigado!",
        content_en: "📝 Booking Change\n\nWe have received your change request. We are processing it and will contact you shortly. Thank you!",
        content_fr: "📝 Modification de Réservation\n\nNous avons reçu votre demande de modification. Nous la traitons et vous contacterons bientôt. Merci!",
        content_de: "📝 Buchungsänderung\n\nWir haben Ihre Änderungsanfrage erhalten. Wir bearbeiten sie und werden Sie in Kürze kontaktieren. Danke!"
    },
    {
        name: "documentacao_necessaria",
        category: "UTILITY",
        content_pt: "📄 Documentação Necessária\n\nPara finalizar a reserva, necessitamos:\n• Carta de condução (válida há mais de 1 ano)\n• Cartão de crédito em nome do condutor\n• Comprovativo de morada\n\nTem tudo?",
        content_en: "📄 Required Documentation\n\nTo complete the booking, we need:\n• Driver's license (valid for more than 1 year)\n• Credit card in driver's name\n• Proof of address\n\nDo you have everything?",
        content_fr: "📄 Documents Requis\n\nPour finaliser la réservation, nous avons besoin de:\n• Permis de conduire (valide depuis plus d'1 an)\n• Carte de crédit au nom du conducteur\n• Justificatif de domicile\n\nAvez-vous tout?",
        content_de: "📄 Erforderliche Unterlagen\n\nUm die Buchung abzuschließen, benötigen wir:\n• Führerschein (mehr als 1 Jahr gültig)\n• Kreditkarte auf den Namen des Fahrers\n• Adressnachweis\n\nHaben Sie alles?"
    }
];

// Expandir templates para todos os idiomas
const languageCodes = {
    pt: 'pt_PT',
    en: 'en',
    fr: 'fr',
    de: 'de'
};

const templates = [];
templatesNegocio.forEach(template => {
    Object.entries(languageCodes).forEach(([lang, code]) => {
        templates.push({
            name: template.name,
            category: template.category,
            language_code: code,
            content_pt: template.content_pt,
            content_en: template.content_en,
            content_fr: template.content_fr,
            content_de: template.content_de
        });
    });
});

// ════════════════════════════════════════════════════════════════════════════
// FUNÇÕES
// ════════════════════════════════════════════════════════════════════════════

async function criarTemplatesWhatsApp() {
    console.log('🚀 Criando TEMPLATES WHATSAPP para aprovação...\n');
    
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
            
            // Aguardar 1 segundo entre cada criação (evitar rate limits)
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.log(`❌ ${template.name} (${template.language_code}) - ERRO: ${error.message}`);
            errorCount++;
        }
    }
    
    console.log(`\n╔════════════════════════════════════╗`);
    console.log(`║   RESUMO - TEMPLATES WHATSAPP      ║`);
    console.log(`╠════════════════════════════════════╣`);
    console.log(`║ ✅ Criados: ${successCount.toString().padStart(2)}                     ║`);
    console.log(`║ ❌ Erros:   ${errorCount.toString().padStart(2)}                     ║`);
    console.log(`║ 📊 Total:   ${templates.length.toString().padStart(2)}                     ║`);
    console.log(`╚════════════════════════════════════╝`);
    
    console.log('\n⏰ Aguarde até 24 horas para aprovação do WhatsApp.');
    console.log('💡 Verifique status com: verificarStatusTemplates()');
}

async function verificarStatusTemplates() {
    await fetch('/api/whatsapp/templates/sync-status', {
        method: 'POST',
        credentials: 'same-origin'
    });
    
    const data = await fetch('/api/whatsapp/templates')
        .then(r => r.json());
    
    const approved = data.templates.filter(t => t.status === 'APPROVED').length;
    const pending = data.templates.filter(t => t.status === 'PENDING').length;
    const rejected = data.templates.filter(t => t.status === 'REJECTED').length;
    
    console.log('\n📊 STATUS DOS TEMPLATES WHATSAPP:');
    console.log(`✅ Aprovados:  ${approved}`);
    console.log(`⏳ Pendentes:  ${pending}`);
    console.log(`❌ Rejeitados: ${rejected}`);
    
    if (approved > 0) {
        console.log('\n✅ Templates aprovados (prontos para usar):');
        data.templates
            .filter(t => t.status === 'APPROVED')
            .forEach(t => console.log(`   • ${t.name} (${t.language_code})`));
    }
}

async function deletarTodosTemplates() {
    console.log('🗑️ Deletando TODOS os templates...\n');
    
    const data = await fetch('/api/whatsapp/templates').then(r => r.json());
    
    let deletedCount = 0;
    for (const template of data.templates) {
        try {
            await fetch(`/api/whatsapp/templates/${template.id}`, {
                method: 'DELETE',
                credentials: 'same-origin'
            });
            console.log(`✅ Deletado: ${template.name} (${template.language_code})`);
            deletedCount++;
        } catch (error) {
            console.log(`❌ Erro ao deletar ${template.name}: ${error.message}`);
        }
    }
    
    console.log(`\n✅ ${deletedCount} templates deletados!`);
}

// ════════════════════════════════════════════════════════════════════════════
// MENSAGEM INICIAL
// ════════════════════════════════════════════════════════════════════════════

console.log('%c╔════════════════════════════════════════════════════════════╗', 'color: #25D366; font-weight: bold');
console.log('%c║      TEMPLATES WHATSAPP - MENSAGENS DE NEGÓCIO            ║', 'color: #25D366; font-weight: bold');
console.log('%c║      Precisam aprovação do WhatsApp (24h)                 ║', 'color: #25D366; font-weight: bold');
console.log('%c╚════════════════════════════════════════════════════════════╝', 'color: #25D366; font-weight: bold');
console.log('\n📋 10 Templates × 4 idiomas = 40 templates total:');
console.log('\n🚗 TEMPLATES DE NEGÓCIO:');
templatesNegocio.forEach((t, i) => console.log(`   ${(i+1).toString().padStart(2)}. ${t.name}`));
console.log('\n🌍 IDIOMAS: Português (pt_PT), Inglês (en), Francês (fr), Alemão (de)');
console.log('\n🚀 Para criar todos os templates:');
console.log('%c   criarTemplatesWhatsApp()', 'color: yellow; font-weight: bold; font-size: 14px');
console.log('\n💡 Para verificar status depois:');
console.log('%c   verificarStatusTemplates()', 'color: cyan; font-weight: bold');
console.log('\n🗑️ Para deletar todos (começar do zero):');
console.log('%c   deletarTodosTemplates()', 'color: red; font-weight: bold');
