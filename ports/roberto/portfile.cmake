

vcpkg_from_git(
    OUT_SOURCE_PATH SOURCE_PATH
    URL git@bitbucket.org:id4tv/roberto.git
    REF 8bc7c0594be3d91fb779f523ed28819d3e331c78
    HEAD_REF master    
)


vcpkg_from_git(
    OUT_SOURCE_PATH SOURCE_PATH_simplylivebase
    URL git@bitbucket.org:id4tv/simplylivebase.git
    REF d327fd6aeef20db635763f402b7d67f60c359587
    HEAD_REF master
)

file(COPY "${SOURCE_PATH_simplylivebase}/" DESTINATION "${SOURCE_PATH}/submodule/simplylivebase")

# Remove exisiting folder in case it was not cleaned
file(REMOVE_RECURSE "${SOURCE_PATH}/submodule/simplylivebase")
# Copy the submodules to the right place
file(COPY "${SOURCE_PATH_simplylivebase}/" DESTINATION "${SOURCE_PATH}/submodule/simplylivebase")

vcpkg_configure_cmake(
  SOURCE_PATH "${SOURCE_PATH}"
  PREFER_NINJA
  OPTIONS
      -DSIMPLYLIVE_GENERATE_TESTEXE=OFF
)

vcpkg_install_cmake()
#vcpkg_fixup_cmake_targets()

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")

file(  INSTALL "${SOURCE_PATH}/CMakeLists.txt"
  DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}"
  RENAME copyright)