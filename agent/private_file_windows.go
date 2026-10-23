//go:build windows

package bee

import (
	"fmt"
	"os"
)

// Temporary fail-closed baseline for native Windows behavioral RED evidence.
// These stubs are replaced only after the tests run on Windows.
func openRegularNoFollow(path string) (*os.File, error) {
	return nil, fmt.Errorf("Windows no-reparse regular-file open is not implemented for %q", path)
}

func validatePrivateFile(file *os.File) error {
	return fmt.Errorf("Windows current-user protected DACL validation is not implemented for %q", file.Name())
}

func writePrivateFile(path string, data []byte, pattern string) error {
	return fmt.Errorf("Windows synced private-file replacement is not implemented for %q", path)
}
