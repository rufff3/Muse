#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = 0;
    int c;

    while ((c = getchar()) != EOF) {
        if (c >= '0' && c <= '9') {
            n = n * 10 + (c - '0');
        } else if (n != 0) {
            break;
        }
    }

    if (n < 2) {
        printf("0\n");
        return 0;
    }

    if (n == 2) {
        printf("1\n");
        return 0;
    }

    size_t size = (size_t)n / 2 + 1;
    unsigned char *composite = calloc(size, sizeof(*composite));
    if (composite == NULL) {
        return 1;
    }

    for (int p = 3; p <= n / p; p += 2) {
        if (!composite[p / 2]) {
            for (int multiple = p * p; multiple <= n; multiple += 2 * p) {
                composite[multiple / 2] = 1;
            }
        }
    }

    int count = 1;
    for (int i = 1; 2 * i + 1 <= n; ++i) {
        if (!composite[i]) {
            ++count;
        }
    }

    free(composite);
    printf("%d\n", count);
    return 0;
}
