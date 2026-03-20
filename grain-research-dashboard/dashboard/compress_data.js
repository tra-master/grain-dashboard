const fs = require('fs');
const path = require('path');

function compressSeasonalData(data) {
    if (typeof data !== 'object' || data === null) {
        return data;
    }
    
    // 检查是否是季节性格式的数据（有 labels 和 datasets）
    if (data.labels && data.datasets) {
        const labels = data.labels;
        const datasets = data.datasets;
        
        const result = {
            labels: labels,
            datasets: {}
        };
        
        for (const spreadName in datasets) {
            const yearData = datasets[spreadName];
            result.datasets[spreadName] = {};
            
            for (const year in yearData) {
                const values = yearData[year];
                if (Array.isArray(values)) {
                    // 提取非null值及其索引
                    const compressed = values.map((v, i) => [i, v]).filter(pair => pair[1] !== null);
                    result.datasets[spreadName][year] = compressed;
                } else {
                    result.datasets[spreadName][year] = values;
                }
            }
        }
        
        return result;
    }
    
    // 递归处理其他字段
    const result = {};
    for (const key in data) {
        result[key] = compressSeasonalData(data[key]);
    }
    return result;
}

function extractAndCompressHtml(inputPath, outputPath) {
    // 读取文件
    let content = fs.readFileSync(inputPath, 'utf-8');
    
    // 找到 EMBEDDED_DATA 的开始和结束
    const pattern = /(const EMBEDDED_DATA = )(\{[\s\S]*?\n\});/;
    const match = content.match(pattern);
    
    if (!match) {
        console.error('错误: 未找到 EMBEDDED_DATA');
        process.exit(1);
    }
    
    const prefix = match[1];  // "const EMBEDDED_DATA = "
    const jsonStr = match[2];  // JSON数据
    
    console.log(`原始JSON长度: ${jsonStr.length} 字符`);
    
    // 解析JSON
    let data;
    try {
        data = JSON.parse(jsonStr);
    } catch (e) {
        console.error(`JSON解析错误: ${e.message}`);
        process.exit(1);
    }
    
    // 压缩数据
    console.log('正在压缩数据...');
    const compressedData = compressSeasonalData(data);
    
    // 重新序列化为JSON
    const compressedJson = JSON.stringify(compressedData);
    console.log(`压缩后JSON长度: ${compressedJson.length} 字符`);
    console.log(`压缩率: ${100 - 100*compressedJson.length/jsonStr.length:.1f}%`);
    
    // 替换内容
    content = content.replace(pattern, prefix + compressedJson + ';');
    
    // 写入输出文件
    fs.writeFileSync(outputPath, content, 'utf-8');
    
    console.log(`已保存到: ${outputPath}`);
}

// 主程序
const inputFile = 'C:\\Users\\administer\\WorkBuddy\\20260315144604\\grain-research-dashboard\\dashboard\\spreads.html';
const outputFile = 'C:\\Users\\administer\\WorkBuddy\\20260315144604\\grain-research-dashboard\\dashboard\\spreads_compressed.html';
const logFile = 'C:\\Users\\administer\\WorkBuddy\\20260315144604\\grain-research-dashboard\\dashboard\\compress_log.txt';

const fs = require('fs');

// 重定向console输出到文件
const logStream = fs.createWriteStream(logFile, {flags: 'a'});
console.log = function(...args) {
    logStream.write(args.join(' ') + '\n');
};
console.error = function(...args) {
    logStream.write('ERROR: ' + args.join(' ') + '\n');
};

console.log('开始压缩...');
try {
    extractAndCompressHtml(inputFile, outputFile);
    console.log('完成!');
} catch(e) {
    console.error('错误:', e.message);
    console.error(e.stack);
}
logStream.end();
