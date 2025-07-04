
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include "xlsxwriter.h"

#define NUM_COLS 64
#define NUM_ROWS 64
#define DATA_DIR "aug_data"

void txt_to_xlsx(const char *txt_filename, const char *xlsx_filename) {
    FILE *fp = fopen(txt_filename, "r");
    if (!fp) {
        fprintf(stderr, "无法打开 %s\n", txt_filename);
        return;
    }

    lxw_workbook  *workbook  = workbook_new(xlsx_filename);
    lxw_worksheet *worksheet = workbook_add_worksheet(workbook, NULL);

    for (int row = 0; row < NUM_ROWS; row++) {
        worksheet_set_row(worksheet, row, 30, NULL);
    }
    worksheet_set_column(worksheet, 0, NUM_COLS - 1, 5, NULL);

    for (int row = 0; row < NUM_ROWS; row++) {
        char line[2048];
        if (!fgets(line, sizeof(line), fp)) {
            fprintf(stderr, "读取 %s 第 %d 行失败\n", txt_filename, row);
            break;
        }

        char *token = strtok(line, " \t\r\n");
        for (int col = 0; token && col < NUM_COLS; col++) {
            double value = atof(token);
            worksheet_write_number(worksheet, row, col, value, NULL);
            token = strtok(NULL, " \t\r\n");
        }
    }

    fclose(fp);
    workbook_close(workbook);
    printf("✅ 已生成：%s\n", xlsx_filename);
}

void traverse_directory(const char *dir_path) {
    DIR *dir = opendir(dir_path);
    if (!dir) {
        perror("无法打开目录");
        return;
    }

    struct dirent *entry;
    char full_path[512];
    char out_path[512];

    while ((entry = readdir(dir)) != NULL) {
        // 忽略 . 和 ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);

        struct stat st;
        if (stat(full_path, &st) == -1) continue;

        if (S_ISDIR(st.st_mode)) {
            // 递归处理子目录
            traverse_directory(full_path);
        } else if (S_ISREG(st.st_mode) && strstr(entry->d_name, ".txt")) {
            // 处理 .txt 文件
            snprintf(out_path, sizeof(out_path), "%s/%.*s.xlsx",
                     dir_path, (int)(strlen(entry->d_name) - 4), entry->d_name);
            txt_to_xlsx(full_path, out_path);
        }
    }

    closedir(dir);
}

int main(void) {
    printf("📁 正在递归查找 %s 目录中的 .txt 文件...\n", DATA_DIR);
    traverse_directory(DATA_DIR);
    return 0;
}

