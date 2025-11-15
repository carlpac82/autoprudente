// Templates WhatsApp para Aluguer de Automóveis
// Cole este código no Console (F12) do browser após fazer login

const templates = [
    {
        name: "confirmacao_interesse",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "Olá! Obrigado pelo seu interesse na Auto Prudente. Tem alguma dúvida sobre aluguer de veículos? Estamos aqui para ajudar!",
        content_en: "Hello! Thank you for your interest in Auto Prudente. Do you have any questions about vehicle rental? We're here to help!",
        content_fr: "Bonjour! Merci pour votre intérêt pour Auto Prudente. Avez-vous des questions sur la location de véhicules? Nous sommes là pour vous aider!",
        content_de: "Hallo! Vielen Dank für Ihr Interesse an Auto Prudente. Haben Sie Fragen zur Fahrzeugmiete? Wir sind hier um zu helfen!"
    },
    {
        name: "confirmacao_reserva",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "✅ Reserva confirmada!\n\nVeículo reservado com sucesso. Receberá em breve todos os detalhes por email. Obrigado por escolher a Auto Prudente!",
        content_en: "✅ Booking confirmed!\n\nVehicle successfully reserved. You will receive all details by email shortly. Thank you for choosing Auto Prudente!",
        content_fr: "✅ Réservation confirmée!\n\nVéhicule réservé avec succès. Vous recevrez tous les détails par email sous peu. Merci d'avoir choisi Auto Prudente!",
        content_de: "✅ Buchung bestätigt!\n\nFahrzeug erfolgreich reserviert. Sie erhalten in Kürze alle Details per E-Mail. Vielen Dank, dass Sie sich für Auto Prudente entschieden haben!"
    },
    {
        name: "lembrete_recolha",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🚗 Lembrete de Recolha\n\nSua recolha do veículo está marcada para amanhã. Por favor confirme sua presença. Obrigado!",
        content_en: "🚗 Pick-up Reminder\n\nYour vehicle pick-up is scheduled for tomorrow. Please confirm your attendance. Thank you!",
        content_fr: "🚗 Rappel de Récupération\n\nVotre récupération du véhicule est prévue pour demain. Veuillez confirmer votre présence. Merci!",
        content_de: "🚗 Abholungs-Erinnerung\n\nIhre Fahrzeugabholung ist für morgen geplant. Bitte bestätigen Sie Ihre Anwesenheit. Danke!"
    },
    {
        name: "instrucoes_checkin",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "📋 Instruções de Check-in\n\nPor favor traga:\n• Carta de condução válida\n• Cartão de crédito\n• Documento de identificação\n\nNos vemos em breve!",
        content_en: "📋 Check-in Instructions\n\nPlease bring:\n• Valid driver's license\n• Credit card\n• ID document\n\nSee you soon!",
        content_fr: "📋 Instructions d'Enregistrement\n\nVeuillez apporter:\n• Permis de conduire valide\n• Carte de crédit\n• Document d'identité\n\nÀ bientôt!",
        content_de: "📋 Check-in Anweisungen\n\nBitte mitbringen:\n• Gültiger Führerschein\n• Kreditkarte\n• Ausweisdokument\n\nBis bald!"
    },
    {
        name: "verificacao_devolucao",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🔄 Verificação de Devolução\n\nLembramos que a devolução do veículo está prevista para amanhã. Por favor confirme o horário. Obrigado pela preferência!",
        content_en: "🔄 Return Check\n\nWe remind you that the vehicle return is scheduled for tomorrow. Please confirm the time. Thank you for your preference!",
        content_fr: "🔄 Vérification du Retour\n\nNous vous rappelons que le retour du véhicule est prévu pour demain. Veuillez confirmer l'heure. Merci pour votre préférence!",
        content_de: "🔄 Rückgabe-Überprüfung\n\nWir erinnern Sie daran, dass die Fahrzeugrückgabe für morgen geplant ist. Bitte bestätigen Sie die Uhrzeit. Vielen Dank für Ihre Präferenz!"
    },
    {
        name: "agradecimento_servico",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🙏 Obrigado!\n\nObrigado por escolher a Auto Prudente. Esperamos que tenha tido uma excelente experiência. Até breve!",
        content_en: "🙏 Thank you!\n\nThank you for choosing Auto Prudente. We hope you had an excellent experience. See you soon!",
        content_fr: "🙏 Merci!\n\nMerci d'avoir choisi Auto Prudente. Nous espérons que vous avez eu une excellente expérience. À bientôt!",
        content_de: "🙏 Danke!\n\nVielen Dank, dass Sie sich für Auto Prudente entschieden haben. Wir hoffen, Sie hatten eine ausgezeichnete Erfahrung. Bis bald!"
    },
    {
        name: "seguimento_orcamento",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "💰 Seguimento de Orçamento\n\nJá recebeu o nosso orçamento? Tem alguma dúvida? Estamos à disposição para ajudar!",
        content_en: "💰 Quote Follow-up\n\nHave you received our quote? Do you have any questions? We're available to help!",
        content_fr: "💰 Suivi du Devis\n\nAvez-vous reçu notre devis? Avez-vous des questions? Nous sommes disponibles pour vous aider!",
        content_de: "💰 Angebots-Nachverfolgung\n\nHaben Sie unser Angebot erhalten? Haben Sie Fragen? Wir stehen Ihnen gerne zur Verfügung!"
    },
    {
        name: "disponibilidade_veiculos",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🚙 Disponibilidade de Veículos\n\nTemos vários veículos disponíveis para as suas datas. Gostaria de saber mais sobre algum modelo em particular?",
        content_en: "🚙 Vehicle Availability\n\nWe have several vehicles available for your dates. Would you like to know more about any particular model?",
        content_fr: "🚙 Disponibilité des Véhicules\n\nNous avons plusieurs véhicules disponibles pour vos dates. Souhaitez-vous en savoir plus sur un modèle particulier?",
        content_de: "🚙 Fahrzeugverfügbarkeit\n\nWir haben mehrere Fahrzeuge für Ihre Termine verfügbar. Möchten Sie mehr über ein bestimmtes Modell erfahren?"
    },
    {
        name: "alteracao_reserva",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "📝 Alteração de Reserva\n\nRecebemos o seu pedido de alteração. Estamos a processar e entraremos em contacto em breve. Obrigado!",
        content_en: "📝 Booking Change\n\nWe have received your change request. We are processing it and will contact you shortly. Thank you!",
        content_fr: "📝 Modification de Réservation\n\nNous avons reçu votre demande de modification. Nous la traitons et vous contacterons bientôt. Merci!",
        content_de: "📝 Buchungsänderung\n\nWir haben Ihre Änderungsanfrage erhalten. Wir bearbeiten sie und werden Sie in Kürze kontaktieren. Danke!"
    },
    {
        name: "documentacao_necessaria",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "📄 Documentação Necessária\n\nPara finalizar a reserva, necessitamos:\n• Carta de condução (válida há mais de 1 ano)\n• Cartão de crédito em nome do condutor\n• Comprovativo de morada\n\nTem tudo?",
        content_en: "📄 Required Documentation\n\nTo complete the booking, we need:\n• Driver's license (valid for more than 1 year)\n• Credit card in driver's name\n• Proof of address\n\nDo you have everything?",
        content_fr: "📄 Documents Requis\n\nPour finaliser la réservation, nous avons besoin de:\n• Permis de conduire (valide depuis plus d'1 an)\n• Carte de crédit au nom du conducteur\n• Justificatif de domicile\n\nAvez-vous tout?",
        content_de: "📄 Erforderliche Unterlagen\n\nUm die Buchung abzuschließen, benötigen wir:\n• Führerschein (mehr als 1 Jahr gültig)\n• Kreditkarte auf den Namen des Fahrers\n• Adressnachweis\n\nHaben Sie alles?"
    },
    // === SAUDAÇÕES E RESPOSTAS RÁPIDAS ===
    {
        name: "bom_dia",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "☀️ Bom dia! Como posso ajudar hoje?",
        content_en: "☀️ Good morning! How can I help you today?",
        content_fr: "☀️ Bonjour! Comment puis-je vous aider aujourd'hui?",
        content_de: "☀️ Guten Morgen! Wie kann ich Ihnen heute helfen?"
    },
    {
        name: "boa_tarde",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🌤️ Boa tarde! Em que posso ser útil?",
        content_en: "🌤️ Good afternoon! How can I be of service?",
        content_fr: "🌤️ Bon après-midi! En quoi puis-je être utile?",
        content_de: "🌤️ Guten Tag! Wie kann ich Ihnen behilflich sein?"
    },
    {
        name: "boa_noite",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🌙 Boa noite! Como posso ajudar?",
        content_en: "🌙 Good evening! How can I help you?",
        content_fr: "🌙 Bonsoir! Comment puis-je vous aider?",
        content_de: "🌙 Guten Abend! Wie kann ich helfen?"
    },
    {
        name: "ola_inicial",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "👋 Olá! Bem-vindo à Auto Prudente. Como posso ajudar?",
        content_en: "👋 Hello! Welcome to Auto Prudente. How can I help you?",
        content_fr: "👋 Bonjour! Bienvenue chez Auto Prudente. Comment puis-je vous aider?",
        content_de: "👋 Hallo! Willkommen bei Auto Prudente. Wie kann ich Ihnen helfen?"
    },
    {
        name: "obrigado_resposta",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🙏 De nada! Estamos sempre à disposição. Precisar de algo mais, é só avisar!",
        content_en: "🙏 You're welcome! We're always available. If you need anything else, just let us know!",
        content_fr: "🙏 De rien! Nous sommes toujours à votre disposition. Si vous avez besoin d'autre chose, faites-le nous savoir!",
        content_de: "🙏 Gern geschehen! Wir stehen Ihnen jederzeit zur Verfügung. Wenn Sie noch etwas brauchen, sagen Sie einfach Bescheid!"
    },
    {
        name: "ate_breve",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "👋 Até breve! Qualquer coisa, estamos aqui.",
        content_en: "👋 See you soon! We're here for anything you need.",
        content_fr: "👋 À bientôt! Nous sommes là pour tout ce dont vous avez besoin.",
        content_de: "👋 Bis bald! Wir sind für alles da, was Sie brauchen."
    },
    {
        name: "disponivel_ajudar",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "💬 Estou disponível para ajudar! O que precisa?",
        content_en: "💬 I'm available to help! What do you need?",
        content_fr: "💬 Je suis disponible pour vous aider! De quoi avez-vous besoin?",
        content_de: "💬 Ich bin verfügbar um zu helfen! Was brauchen Sie?"
    },
    {
        name: "um_momento",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "⏳ Um momento, por favor. Já verifico isso para si!",
        content_en: "⏳ One moment, please. I'll check that for you right away!",
        content_fr: "⏳ Un instant, s'il vous plaît. Je vérifie cela pour vous tout de suite!",
        content_de: "⏳ Einen Moment bitte. Ich prüfe das sofort für Sie!"
    },
    {
        name: "entendi_pedido",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "✅ Entendido! Vou tratar do seu pedido imediatamente.",
        content_en: "✅ Understood! I'll take care of your request immediately.",
        content_fr: "✅ Compris! Je m'occupe de votre demande immédiatement.",
        content_de: "✅ Verstanden! Ich kümmere mich sofort um Ihre Anfrage."
    },
    {
        name: "com_prazer",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "😊 Com todo o prazer! É sempre um prazer ajudar.",
        content_en: "😊 With pleasure! It's always a pleasure to help.",
        content_fr: "😊 Avec plaisir! C'est toujours un plaisir d'aider.",
        content_de: "😊 Mit Vergnügen! Es ist immer eine Freude zu helfen."
    },
    {
        name: "excelente_escolha",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "⭐ Excelente escolha! Vou processar isso agora mesmo.",
        content_en: "⭐ Excellent choice! I'll process that right now.",
        content_fr: "⭐ Excellent choix! Je vais traiter cela tout de suite.",
        content_de: "⭐ Ausgezeichnete Wahl! Ich werde das jetzt bearbeiten."
    },
    {
        name: "sem_problema",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "👍 Sem problema! Fico feliz em poder ajudar.",
        content_en: "👍 No problem! Happy to help.",
        content_fr: "👍 Pas de problème! Heureux de pouvoir vous aider.",
        content_de: "👍 Kein Problem! Ich helfe gerne."
    },
    {
        name: "pronto_ajudar",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "✨ Pronto para ajudar! Diga-me como posso ser útil.",
        content_en: "✨ Ready to help! Tell me how I can be useful.",
        content_fr: "✨ Prêt à vous aider! Dites-moi comment je peux être utile.",
        content_de: "✨ Bereit zu helfen! Sagen Sie mir, wie ich nützlich sein kann."
    },
    {
        name: "bom_fim_semana",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🎉 Bom fim de semana! Qualquer coisa, conte connosco.",
        content_en: "🎉 Have a great weekend! If you need anything, count on us.",
        content_fr: "🎉 Bon week-end! Si vous avez besoin de quoi que ce soit, comptez sur nous.",
        content_de: "🎉 Schönes Wochenende! Wenn Sie etwas brauchen, zählen Sie auf uns."
    },
    {
        name: "otimo_dia",
        category: "UTILITY",
        language_code: "pt",
        content_pt: "🌟 Tenha um ótimo dia! Estamos sempre por aqui.",
        content_en: "🌟 Have a great day! We're always around.",
        content_fr: "🌟 Passez une excellente journée! Nous sommes toujours là.",
        content_de: "🌟 Haben Sie einen großartigen Tag! Wir sind immer in der Nähe."
    }
];

// Função para criar todos os templates
async function criarTodosTemplates() {
    console.log('🚀 Criando templates para aluguer de automóveis...\n');
    
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
                console.log(`✅ ${template.name} - CRIADO E ENVIADO`);
                successCount++;
            } else {
                console.log(`❌ ${template.name} - ERRO: ${result.error}`);
                errorCount++;
            }
            
            // Aguardar 1 segundo entre cada criação (evitar rate limits)
            await new Promise(resolve => setTimeout(resolve, 1000));
            
        } catch (error) {
            console.log(`❌ ${template.name} - ERRO: ${error.message}`);
            errorCount++;
        }
    }
    
    console.log(`\n╔════════════════════════════════════╗`);
    console.log(`║       RESUMO DA CRIAÇÃO            ║`);
    console.log(`╠════════════════════════════════════╣`);
    console.log(`║ ✅ Criados: ${successCount.toString().padStart(2)}                     ║`);
    console.log(`║ ❌ Erros:   ${errorCount.toString().padStart(2)}                     ║`);
    console.log(`║ 📊 Total:   ${templates.length.toString().padStart(2)}                     ║`);
    console.log(`╚════════════════════════════════════╝`);
    
    console.log('\n⏰ Aguarde até 24 horas para aprovação do WhatsApp.');
    console.log('💡 Verifique status com: await verificarStatusTemplates();');
}

// Função para verificar status
async function verificarStatusTemplates() {
    const response = await fetch('/api/whatsapp/templates/sync-status', {
        method: 'POST',
        credentials: 'same-origin'
    });
    
    const templates = await fetch('/api/whatsapp/templates')
        .then(r => r.json());
    
    const approved = templates.templates.filter(t => t.status === 'APPROVED').length;
    const pending = templates.templates.filter(t => t.status === 'PENDING').length;
    const rejected = templates.templates.filter(t => t.status === 'REJECTED').length;
    
    console.log('\n📊 STATUS DOS TEMPLATES:');
    console.log(`✅ Aprovados:  ${approved}`);
    console.log(`⏳ Pendentes:  ${pending}`);
    console.log(`❌ Rejeitados: ${rejected}`);
    
    if (approved > 0) {
        console.log('\n✅ Templates aprovados (prontos para usar):');
        templates.templates
            .filter(t => t.status === 'APPROVED')
            .forEach(t => console.log(`   • ${t.name}`));
    }
}

// EXECUTAR CRIAÇÃO
console.log('%c╔════════════════════════════════════════════════╗', 'color: #25D366; font-weight: bold');
console.log('%c║  TEMPLATES WHATSAPP - ALUGUER DE AUTOMÓVEIS   ║', 'color: #25D366; font-weight: bold');
console.log('%c╚════════════════════════════════════════════════╝', 'color: #25D366; font-weight: bold');
console.log('\n📋 25 Templates prontos para criar:');
console.log('\n🚗 NEGÓCIO (10):');
templates.slice(0, 10).forEach((t, i) => console.log(`   ${i+1}. ${t.name}`));
console.log('\n💬 SAUDAÇÕES E RESPOSTAS RÁPIDAS (15):');
templates.slice(10).forEach((t, i) => console.log(`   ${i+11}. ${t.name}`));
console.log('\n🚀 Para criar todos os templates, execute:');
console.log('%c   criarTodosTemplates()', 'color: yellow; font-weight: bold; font-size: 14px');
console.log('\n💡 Para verificar status depois:');
console.log('%c   verificarStatusTemplates()', 'color: cyan; font-weight: bold');
