// ╔════════════════════════════════════════════════════════════════════════════╗
// ║  QUICK REPLIES - RESPOSTAS RÁPIDAS DENTRO DE CONVERSAS                    ║
// ║  NÃO precisam aprovação do WhatsApp                                        ║
// ║  Usadas DENTRO de conversas ativas (janela de 24 horas)                   ║
// ╚════════════════════════════════════════════════════════════════════════════╝

// Cole este código no Console (F12) do browser na página Admin → WhatsApp

const quickRepliesBase = [
    {
        shortcut: "bom_dia",
        content_pt: "☀️ Bom dia! Como posso ajudar hoje?",
        content_en: "☀️ Good morning! How can I help you today?",
        content_fr: "☀️ Bonjour! Comment puis-je vous aider aujourd'hui?",
        content_de: "☀️ Guten Morgen! Wie kann ich Ihnen heute helfen?"
    },
    {
        shortcut: "boa_tarde",
        content_pt: "🌤️ Boa tarde! Em que posso ser útil?",
        content_en: "🌤️ Good afternoon! How can I be of service?",
        content_fr: "🌤️ Bon après-midi! En quoi puis-je être utile?",
        content_de: "🌤️ Guten Tag! Wie kann ich Ihnen behilflich sein?"
    },
    {
        shortcut: "boa_noite",
        content_pt: "🌙 Boa noite! Como posso ajudar?",
        content_en: "🌙 Good evening! How can I help you?",
        content_fr: "🌙 Bonsoir! Comment puis-je vous aider?",
        content_de: "🌙 Guten Abend! Wie kann ich helfen?"
    },
    {
        shortcut: "ola",
        content_pt: "👋 Olá! Bem-vindo à Auto Prudente. Como posso ajudar?",
        content_en: "👋 Hello! Welcome to Auto Prudente. How can I help you?",
        content_fr: "👋 Bonjour! Bienvenue chez Auto Prudente. Comment puis-je vous aider?",
        content_de: "👋 Hallo! Willkommen bei Auto Prudente. Wie kann ich Ihnen helfen?"
    },
    {
        shortcut: "obrigado",
        content_pt: "🙏 De nada! Estamos sempre à disposição. Precisar de algo mais, é só avisar!",
        content_en: "🙏 You're welcome! We're always available. If you need anything else, just let us know!",
        content_fr: "🙏 De rien! Nous sommes toujours à votre disposition. Si vous avez besoin d'autre chose, faites-le nous savoir!",
        content_de: "🙏 Gern geschehen! Wir stehen Ihnen jederzeit zur Verfügung. Wenn Sie noch etwas brauchen, sagen Sie einfach Bescheid!"
    },
    {
        shortcut: "ate_breve",
        content_pt: "👋 Até breve! Qualquer coisa, estamos aqui.",
        content_en: "👋 See you soon! We're here for anything you need.",
        content_fr: "👋 À bientôt! Nous sommes là pour tout ce dont vous avez besoin.",
        content_de: "👋 Bis bald! Wir sind für alles da, was Sie brauchen."
    },
    {
        shortcut: "disponivel",
        content_pt: "💬 Estou disponível para ajudar! O que precisa?",
        content_en: "💬 I'm available to help! What do you need?",
        content_fr: "💬 Je suis disponible pour vous aider! De quoi avez-vous besoin?",
        content_de: "💬 Ich bin verfügbar um zu helfen! Was brauchen Sie?"
    },
    {
        shortcut: "momento",
        content_pt: "⏳ Um momento, por favor. Já verifico isso para si!",
        content_en: "⏳ One moment, please. I'll check that for you right away!",
        content_fr: "⏳ Un instant, s'il vous plaît. Je vérifie cela pour vous tout de suite!",
        content_de: "⏳ Einen Moment bitte. Ich prüfe das sofort für Sie!"
    },
    {
        shortcut: "entendido",
        content_pt: "✅ Entendido! Vou tratar do seu pedido imediatamente.",
        content_en: "✅ Understood! I'll take care of your request immediately.",
        content_fr: "✅ Compris! Je m'occupe de votre demande immédiatement.",
        content_de: "✅ Verstanden! Ich kümmere mich sofort um Ihre Anfrage."
    },
    {
        shortcut: "prazer",
        content_pt: "😊 Com todo o prazer! É sempre um prazer ajudar.",
        content_en: "😊 With pleasure! It's always a pleasure to help.",
        content_fr: "😊 Avec plaisir! C'est toujours un plaisir d'aider.",
        content_de: "😊 Mit Vergnügen! Es ist immer eine Freude zu helfen."
    },
    {
        shortcut: "excelente",
        content_pt: "⭐ Excelente escolha! Vou processar isso agora mesmo.",
        content_en: "⭐ Excellent choice! I'll process that right now.",
        content_fr: "⭐ Excellent choix! Je vais traiter cela tout de suite.",
        content_de: "⭐ Ausgezeichnete Wahl! Ich werde das jetzt bearbeiten."
    },
    {
        shortcut: "sem_problema",
        content_pt: "👍 Sem problema! Fico feliz em poder ajudar.",
        content_en: "👍 No problem! Happy to help.",
        content_fr: "👍 Pas de problème! Heureux de pouvoir vous aider.",
        content_de: "👍 Kein Problem! Ich helfe gerne."
    },
    {
        shortcut: "pronto",
        content_pt: "✨ Pronto para ajudar! Diga-me como posso ser útil.",
        content_en: "✨ Ready to help! Tell me how I can be useful.",
        content_fr: "✨ Prêt à vous aider! Dites-moi comment je peux être utile.",
        content_de: "✨ Bereit zu helfen! Sagen Sie mir, wie ich nützlich sein kann."
    },
    {
        shortcut: "bom_fim_semana",
        content_pt: "🎉 Bom fim de semana! Qualquer coisa, conte connosco.",
        content_en: "🎉 Have a great weekend! If you need anything, count on us.",
        content_fr: "🎉 Bon week-end! Si vous avez besoin de quoi que ce soit, comptez sur nous.",
        content_de: "🎉 Schönes Wochenende! Wenn Sie etwas brauchen, zählen Sie auf uns."
    },
    {
        shortcut: "otimo_dia",
        content_pt: "🌟 Tenha um ótimo dia! Estamos sempre por aqui.",
        content_en: "🌟 Have a great day! We're always around.",
        content_fr: "🌟 Passez une excellente journée! Nous sommes toujours là.",
        content_de: "🌟 Haben Sie einen großartigen Tag! Wir sind immer in der Nähe."
    }
];

// Expandir para todos os idiomas
const languageCodes = {
    pt: 'pt_PT',
    en: 'en',
    fr: 'fr',
    de: 'de'
};

const quickReplies = [];
quickRepliesBase.forEach(reply => {
    Object.entries(languageCodes).forEach(([lang, code]) => {
        const content = reply[`content_${lang}`];
        quickReplies.push({
            shortcut: `${reply.shortcut}_${lang}`,
            message: content,
            language: code
        });
    });
});

// ════════════════════════════════════════════════════════════════════════════
// FUNÇÕES
// ════════════════════════════════════════════════════════════════════════════

async function criarQuickReplies() {
    console.log('🚀 Criando QUICK REPLIES (respostas rápidas)...\n');
    
    let successCount = 0;
    let errorCount = 0;
    
    for (const reply of quickReplies) {
        try {
            const response = await fetch('/api/whatsapp/quick-replies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify(reply)
            });
            
            const result = await response.json();
            
            if (result.ok || result.success) {
                console.log(`✅ ${reply.shortcut} - CRIADO`);
                successCount++;
            } else {
                console.log(`❌ ${reply.shortcut} - ERRO: ${result.error || result.message}`);
                errorCount++;
            }
            
            // Aguardar 200ms entre cada criação
            await new Promise(resolve => setTimeout(resolve, 200));
            
        } catch (error) {
            console.log(`❌ ${reply.shortcut} - ERRO: ${error.message}`);
            errorCount++;
        }
    }
    
    console.log(`\n╔════════════════════════════════════╗`);
    console.log(`║     RESUMO - QUICK REPLIES         ║`);
    console.log(`╠════════════════════════════════════╣`);
    console.log(`║ ✅ Criados: ${successCount.toString().padStart(2)}                     ║`);
    console.log(`║ ❌ Erros:   ${errorCount.toString().padStart(2)}                     ║`);
    console.log(`║ 📊 Total:   ${quickReplies.length.toString().padStart(2)}                     ║`);
    console.log(`╚════════════════════════════════════╝`);
    
    console.log('\n✅ Quick Replies NÃO precisam aprovação!');
    console.log('💡 Já estão prontas para usar no chat!');
}

async function listarQuickReplies() {
    const data = await fetch('/api/whatsapp/quick-replies')
        .then(r => r.json());
    
    console.log('\n📋 QUICK REPLIES EXISTENTES:\n');
    
    if (data.replies && data.replies.length > 0) {
        const porIdioma = {};
        data.replies.forEach(r => {
            if (!porIdioma[r.language]) porIdioma[r.language] = [];
            porIdioma[r.language].push(r);
        });
        
        Object.entries(porIdioma).forEach(([lang, replies]) => {
            console.log(`\n🌍 ${lang.toUpperCase()} (${replies.length} respostas):`);
            replies.forEach(r => {
                console.log(`   • /${r.shortcut}`);
                console.log(`     ${r.message}`);
            });
        });
        
        console.log(`\n📊 Total: ${data.replies.length} quick replies`);
    } else {
        console.log('⚠️ Nenhuma quick reply encontrada.');
    }
}

async function deletarTodasQuickReplies() {
    console.log('🗑️ Deletando TODAS as quick replies...\n');
    
    const data = await fetch('/api/whatsapp/quick-replies').then(r => r.json());
    
    if (!data.replies || data.replies.length === 0) {
        console.log('⚠️ Nenhuma quick reply para deletar.');
        return;
    }
    
    let deletedCount = 0;
    for (const reply of data.replies) {
        try {
            await fetch(`/api/whatsapp/quick-replies/${reply.id}`, {
                method: 'DELETE',
                credentials: 'same-origin'
            });
            console.log(`✅ Deletado: ${reply.shortcut}`);
            deletedCount++;
        } catch (error) {
            console.log(`❌ Erro ao deletar ${reply.shortcut}: ${error.message}`);
        }
    }
    
    console.log(`\n✅ ${deletedCount} quick replies deletadas!`);
}

// ════════════════════════════════════════════════════════════════════════════
// MENSAGEM INICIAL
// ════════════════════════════════════════════════════════════════════════════

console.log('%c╔════════════════════════════════════════════════════════════╗', 'color: #128C7E; font-weight: bold');
console.log('%c║           QUICK REPLIES - RESPOSTAS RÁPIDAS               ║', 'color: #128C7E; font-weight: bold');
console.log('%c║           NÃO precisam aprovação do WhatsApp              ║', 'color: #128C7E; font-weight: bold');
console.log('%c╚════════════════════════════════════════════════════════════╝', 'color: #128C7E; font-weight: bold');
console.log('\n📋 15 Respostas × 4 idiomas = 60 quick replies total:');
console.log('\n💬 QUICK REPLIES:');
quickRepliesBase.forEach((r, i) => console.log(`   ${(i+1).toString().padStart(2)}. ${r.shortcut}`));
console.log('\n🌍 IDIOMAS: Português (pt_PT), Inglês (en), Francês (fr), Alemão (de)');
console.log('\n🚀 Para criar todas as quick replies:');
console.log('%c   criarQuickReplies()', 'color: yellow; font-weight: bold; font-size: 14px');
console.log('\n💡 Para listar quick replies existentes:');
console.log('%c   listarQuickReplies()', 'color: cyan; font-weight: bold');
console.log('\n🗑️ Para deletar todas (começar do zero):');
console.log('%c   deletarTodasQuickReplies()', 'color: red; font-weight: bold');
