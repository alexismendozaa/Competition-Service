echo "Iniciando revisión estática de sintaxis con pylint..."

find .. -type f -name "*.py" ! -path "*/__pycache__/*" ! -path "*/venv/*" ! -path "*/env/*" > files.txt

while IFS= read -r file; do
    echo "Revisando: $file"
    pylint "$file"
done < files.txt

rm files.txt

echo "Revisión completada." 
