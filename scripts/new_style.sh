#!/bin/bash
set -e

STYLE_NAME=$1

if [ -z "$STYLE_NAME" ]; then
    echo "错误: 请提供风格名称。"
    echo "用法: ./scripts/new_style.sh <style_name>"
    echo ""
    echo "示例: ./scripts/new_style.sh nature_reviews"
    exit 1
fi

STYLE_DIR="mmcs/styles/$STYLE_NAME"

if [ -d "$STYLE_DIR" ]; then
    echo "提示: 风格 '$STYLE_NAME' 已存在 ($STYLE_DIR)"
    exit 1
fi

mkdir -p "$STYLE_DIR"

# --- 生成基础 .mplstyle ---
cat > "$STYLE_DIR/$STYLE_NAME.mplstyle" << 'STYLEEOF'
font.family : sans-serif
font.sans-serif : Arial, Helvetica, DejaVu Sans
axes.labelweight : bold
axes.titleweight : bold
axes.linewidth : 1.5
axes.spines.top : False
axes.spines.right : False
xtick.major.width : 1.5
ytick.major.width : 1.5
xtick.major.size : 6
ytick.major.size : 6
xtick.labelsize : 12
ytick.labelsize : 12
axes.labelsize : 14
axes.titlesize : 16
STYLEEOF

# --- 生成 metadata.json ---
cat > "$STYLE_DIR/metadata.json" << JSONEOF
{
    "name": "$STYLE_NAME",
    "category": "$(echo "$STYLE_NAME" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g')",
    "display_name": "$(echo "$STYLE_NAME" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g') Style",
    "chart_types": [],
    "description": "Description of the $STYLE_NAME style",
    "base_style": "$STYLE_NAME.mplstyle",
    "chart_styles": {}
}
JSONEOF

echo ""
echo "已创建风格家族: $STYLE_DIR"
echo ""
echo "  $(ls $STYLE_DIR/)"
echo ""
echo "后续步骤:"
echo "  1. 编辑 $STYLE_DIR/$STYLE_NAME.mplstyle 调整基础样式参数"
echo "  2. 添加图表类型专用样式, 例如: touch $STYLE_DIR/bar.mplstyle"
echo "  3. 编辑 $STYLE_DIR/metadata.json 声明兼容的 chart_types 和 chart_styles"
echo "  4. 在 examples/ 下编写示例脚本"
