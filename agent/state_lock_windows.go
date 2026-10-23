//go:build windows

package bee

import "fmt"

// Temporary fail-closed baseline for native Windows behavioral RED evidence.
func lockState(path string) (func(), error) {
	return nil, fmt.Errorf("Windows exclusive configuration LockFileEx is not implemented for %q", path+".lock")
}
