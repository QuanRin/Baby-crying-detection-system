import 'package:tinyguard/enums.dart';

class FlavorConfig {
  final Flavor flavor;
  final String baseApiUrl;
  final String versionApi;

  static FlavorConfig? _instance;

  const FlavorConfig._({
    required this.flavor,
    required this.baseApiUrl,
    required this.versionApi,
  });

  factory FlavorConfig({
    required Flavor flavor,
    required String baseApiUrl,
    required String versionAPI,
  }) {
    return _instance ??= FlavorConfig._(
      flavor: flavor,
      baseApiUrl: baseApiUrl,
      versionApi: versionAPI,
    );
  }

  static FlavorConfig get instance => _instance!;

  static bool isProduction() => _instance?.flavor == Flavor.production;

  static bool isDevelopment() => _instance?.flavor == Flavor.development;

  static bool isStaging() => _instance?.flavor == Flavor.staging;

  String get baseURL => '$baseApiUrl$versionApi';
}
