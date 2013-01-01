A SNL(a Pascal like language) Compiler's Frontend(with lexical-analysis and syntactic analysis only)

*Run*
================================================================================
1. You need a Python envirament(Python is installed by default in many Linux machines).

   If you don't, please download and install Python according to your operating system at http://www.python.org/getit/.

2. In Linux, Follow those steps:

   tar xzvf snl_frontend.tar.gz

   cd snl_frontend

   chmod +x make.sh

   ./make.sh

   Then two new file named syntactic_analysis.txt and lexical_analysis.txt is created.

   Check the new file lexical_analysis.txt. It saved the result of bubble_sort.snl's lexical analysis.

   Check the new file syntactic_analysis.txt. It saved the result of bubble_sort.snl's syntactic analysis.

   You can also compile your own source file by command in the present directory:

   python main.py your_own_file > target_file.txt

3. In Windows, Follow those steps:

   Put python in your PATH

   Extract snl_frontend.tar.gz

   In a console, enter directory snl_frontend

   python main.py bubble_sort.snl > target_file.txt

   Then two new file named syntactic_analysis.txt and lexical_analysis.txt is created.

   Check the new file lexical_analysis.txt. It saved the result of bubble_sort.snl's lexical analysis.

   Check the new file syntactic_analysis.txt. It saved the result of bubble_sort.snl's syntactic analysis.

   You can also compile your own source file by command in the present directory:

   python main.py your_own_file > target_file.txt
