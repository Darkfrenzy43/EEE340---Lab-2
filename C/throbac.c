/*
C implementations of the Throbac string concatenation function
`__throbac_cat` (provided for you) and the two Throbac built-in
functions `stringlength` and `substring`

Author: OCdt Aaron Brown and OCdt Liethan Velasco

Version: 2022-01-23
*/

#include <stdlib.h>
#include <string.h>

#include "throbac.h"

char *__throbac_cat(char *first, char *second) {
    size_t length = strlen(first) + strlen(second) + 1;
    void *value = malloc(length);
    if (value == 0) {
        abort();
    }
    strcpy((char *) value, first);
    return strcat((char *) value, second);
}


/*
    Description:

        Compute and return length of inputted string.

    Arguments:
        <char* str> : The string to have its length returned.

    Returns:
        The length of the inputted string.
*/
int stringlength(char* str) {

    // Iterate through str until we hit null character.
    // Count number of iterations.
    int counter = 0;
    while (*str) {
        str++;
        counter++;
    }

    // Return counter value
    return counter;

}

/*

    Description:

        Returns a substring of an inputted string.
        Portion of the string to return specified by arguments.

    Arguments:
        <char* str> : The string to take a substring of.
        <int start> : The starting index of the substring to take.
        <int length> : The length of the substring to take.

    Returns:
        A string pointer to the set substring.
        Returns NULL if an error occurred.

*/

char* substring(char* str, int start, int length) {

    // Needed for bad input handling
    int strLen = stringlength(str);

    // Check if start negative value.
    if (start < 0 || length < 0) {
        printf("\nERROR: Inputted values can't be negative.");
        return NULL;
    }

    // Check if start and length values exceeds strLen
    if (start > (strLen - 1)) {
        printf("\nERROR: Inputted start index larger than string length.");
        return NULL;
    }
    else if (start + length > strLen) {
        printf("\nERROR: Inputted start index and length exceeds string length.");
        return NULL;
    }

    // Otherwise, create substring using malloc
    char* subStr = (char*) malloc(sizeof(char) * length + 1);
    // subStr[length] = '\0';

    // Push str pointer over to start index, then retrieve substring
    str += start;
    for (int i = 0; i < length; i++) {
        *subStr = *str;
        subStr++;
        str++;
    }
    *subStr = '\0';

    // Return subStr pointer to front and return it
    subStr -= length;
    return subStr;
}
