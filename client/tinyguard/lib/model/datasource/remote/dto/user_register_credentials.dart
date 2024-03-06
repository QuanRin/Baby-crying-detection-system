class UserRegisterCredentials {
  final String email;
  final String phone_number;
  final String password;

  UserRegisterCredentials({
    required this.email,
    required this.phone_number,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'phone_number': phone_number,
      'password': password,
    };
  }
}
