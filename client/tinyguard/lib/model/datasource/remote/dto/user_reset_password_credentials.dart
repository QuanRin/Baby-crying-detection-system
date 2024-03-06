class UserResetPasswordCredentials {
  final String email;
  final DateTime date;

  UserResetPasswordCredentials({
    required this.email,
    required this.date,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'date': date,
    };
  }
}
