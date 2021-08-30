---
layout: post
title: Messing around with C
author: matt_sosna
---

Curious to see that you can see the values stored at a location in memory outside your array.

If you're on a Mac, you can compile your code in the Terminal with `cc <filename.c> -o <program_name>` and then run it with `./<program_name>`.

Here's the standard, what we should expect.

{% include header-c.html %}
```c
#include <stdio.h>

int main()
{
    int lost[] = {4, 8, 15, 16, 23, 42};
    size_t n = sizeof(lost) / sizeof(int);

    for(int i=0; i < n; i++){
        printf("%c ", lost[i]);
    }

    return 0;
}
```

When we run this, we get:

{% include header-bash.html %}
```bash
4 8 15 16 23 42 %
```

Great. But now let's start messing around a bit.

## Too few or too many elements
Above, we defined `lost` as an array without specifying the number of elements, i.e. `lost[]`. The array gets initialized to the number of values we pass in, and it's set there afterwards. But we can also define the number upfront, like this:

```c
int lost[6] = {4, 8, 15, 16, 23, 42};
```

If we specify too few elements, nothing happens - the remainder of the array is filled with 0s. Meanwhile, if we specify too many elements, our compiler raises a warning and then simply drops the excess elements from our array.

{% include header-c.html %}
```c
#include <stdio.h>

/* Define variables */

// Valid
int lost1[] = {4, 8, 15, 16, 23, 42};
int lost2[6] = {4, 8, 15, 16, 23, 42};

// Extra space or not enough space
int lost3[10] = {4, 8, 15, 16, 23, 42};
int lost4[3] = {4, 8, 15, 16, 23, 42};

// Get length of each array
size_t n1 = sizeof(lost1)/sizeof(lost1[0]);
size_t n2 = sizeof(lost2)/sizeof(lost2[0]);
size_t n3 = sizeof(lost3)/sizeof(lost3[0]);
size_t n4 = sizeof(lost4)/sizeof(lost4[0]);

int main()
{
    int i;

    // lost1[]
    printf("lost1[]:   ");
    for(i=0; i<n1; i++){
        printf("%d ", lost1[i]);
    }
    printf("\n");

    // lost2[6]
    printf("lost2[6]:  ");
    for(i=0; i<n1; i++){
        printf("%d ", lost2[i]);
    }
    printf("\n");

    // lost3[10]
    printf("lost3[10]: ");
    for(i=0; i<n1; i++){
        printf("%d ", lost3[i]);
    }
    printf("\n");

    // lost4[3]
    printf("lost4[3]:  ");
    for(i=0; i<n1; i++){
        printf("%d ", lost4[i]);
    }

    return 0;

}
```

When we compile this, we get the warning for `lost4[3]`. But we can then move forward and run our script.

{% include header-bash.html %}
```bash
4 8 15 16 23 42
4 8 15 16 23 42
4 8 15 16 23 42
4 8 15 0 6 0 %
```
