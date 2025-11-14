// DIAGNOSTICO DE HIERARQUIA
// Cola este codigo na consola do browser

(function() {
    console.log('========================================');
    console.log('DIAGNOSTICO DE HIERARQUIA');
    console.log('========================================');
    
    // 1. Verificar se a funcao existe
    console.log('\n1. FUNCAO applyGroupHierarchyRules:');
    console.log('   Existe?', typeof applyGroupHierarchyRules);
    
    // 2. Verificar configuracoes no localStorage
    console.log('\n2. CONFIGURACOES (localStorage):');
    const settings = JSON.parse(localStorage.getItem('priceAutomationSettings') || '{}');
    console.log('   enableGroupHierarchy:', settings.enableGroupHierarchy);
    console.log('   Numero de regras:', Object.keys(settings.groupHierarchyRules || {}).length);
    console.log('   Regras:', settings.groupHierarchyRules);
    
    // 3. Verificar localizacao atual
    console.log('\n3. LOCALIZACAO:');
    const location = document.getElementById('locationAuto')?.value;
    console.log('   Atual:', location);
    
    // 4. Verificar dias selecionados
    console.log('\n4. DIAS SELECIONADOS:');
    console.log('   selectedDaysAuto:', window.selectedDaysAuto);
    
    // 5. Verificar precos na tabela
    console.log('\n5. PRECOS NA TABELA:');
    const pricesInTable = {};
    document.querySelectorAll('#pricesTableAuto input[data-type="auto"]').forEach(input => {
        const group = input.dataset.grupo;
        const day = input.dataset.dias;
        const value = input.value;
        
        if (value && parseFloat(value) > 0) {
            if (!pricesInTable[group]) pricesInTable[group] = {};
            pricesInTable[group][day] = parseFloat(value);
        }
    });
    console.log('   Grupos com precos:', Object.keys(pricesInTable));
    console.log('   Detalhes:', pricesInTable);
    
    // 6. Simular aplicacao de hierarquia
    console.log('\n6. SIMULACAO DE HIERARQUIA:');
    const rules = settings.groupHierarchyRules || {};
    
    for (const [targetGroup, dependencies] of Object.entries(rules)) {
        console.log(`\n   Grupo ${targetGroup}:`);
        console.log(`      Dependencias:`, dependencies);
        
        if (!pricesInTable[targetGroup]) {
            console.log(`      Sem precos para ${targetGroup}`);
            continue;
        }
        
        for (const day in pricesInTable[targetGroup]) {
            const targetPrice = pricesInTable[targetGroup][day];
            console.log(`\n      Dia ${day}: ${targetPrice.toFixed(2)} EUR`);
            
            for (const dep of dependencies) {
                const depGroup = typeof dep === 'string' ? dep : dep.group;
                const operator = typeof dep === 'string' ? '>=' : dep.operator;
                const percentage = (typeof dep === 'object' && dep.percentage !== undefined) ? dep.percentage : 0;
                
                const depPrice = pricesInTable[depGroup]?.[day];
                
                if (!depPrice) {
                    console.log(`         ${depGroup} nao tem preco para dia ${day}`);
                    continue;
                }
                
                // Check violation
                let violated = false;
                let requiredPrice = targetPrice;
                
                switch(operator) {
                    case '>=':
                        if (targetPrice < depPrice) {
                            violated = true;
                            requiredPrice = depPrice;
                        }
                        break;
                    case '>':
                        if (targetPrice <= depPrice) {
                            violated = true;
                            requiredPrice = depPrice + 0.01;
                        }
                        break;
                }
                
                if (violated) {
                    console.log(`         VIOLACAO: ${targetGroup}(${targetPrice.toFixed(2)} EUR) ${operator} ${depGroup}(${depPrice.toFixed(2)} EUR)`);
                    console.log(`            Deveria ser: ${requiredPrice.toFixed(2)} EUR`);
                } else {
                    console.log(`         OK: ${targetGroup}(${targetPrice.toFixed(2)} EUR) ${operator} ${depGroup}(${depPrice.toFixed(2)} EUR)`);
                }
            }
        }
    }
    
    // 7. Verificar versao do codigo
    console.log('\n7. VERSAO DO CODIGO:');
    const scriptTags = document.querySelectorAll('script');
    let foundVersion = false;
    scriptTags.forEach(script => {
        const text = script.textContent;
        if (text && text.includes('[VERSION-CHECK]')) {
            const match = text.match(/Code version: ([\d-:]+)/);
            if (match) {
                console.log('   Versao encontrada:', match[1]);
                foundVersion = true;
            }
        }
    });
    if (!foundVersion) {
        console.log('   Versao nao encontrada no codigo');
    }
    
    console.log('\n========================================');
    console.log('DIAGNOSTICO COMPLETO');
    console.log('========================================\n');
})();
